import numpy as np

class HMMManual:
    def __init__(self, n_states=5, n_mix=1, n_iter=10):
        self.n_states = n_states
        self.n_mix = n_mix # Single Gaussian for now typically, or GMM
        self.n_iter = n_iter
        
        # Parameters
        self.pi = None # Initial state distribution
        self.A = None  # Transition matrix
        self.means = None # Means for each state (if Single Gaussian)
        self.covs = None  # Covariances for each state
        
        # If GMM, we would need weights, multiple means/covs per state
        # For simplicity in this "Manual" version, let's start with Single Gaussian per State (GMM with M=1)
        # It's easier to verify code correctness first.

    def _init_params(self, X):
        """
        Initialize parameters based on data X (N_samples, n_features)
        """
        n_samples, n_features = X.shape
        
        # Uniform initialization for A and Pi
        self.pi = np.ones(self.n_states) / self.n_states
        self.A = np.ones((self.n_states, self.n_states)) / self.n_states
        
        # K-Means like initialization for Means (split data into chunks)
        # Or just random selection
        indices = np.array_split(np.arange(n_samples), self.n_states)
        self.means = np.zeros((self.n_states, n_features))
        self.covs = np.zeros((self.n_states, n_features))
        
        for s in range(self.n_states):
            # Assign segment of data to state s to init mean/cov
            segment = X[indices[s]]
            if len(segment) > 0:
                self.means[s] = np.mean(segment, axis=0)
                self.covs[s] = np.var(segment, axis=0) + 1e-4 # Add floor
            else:
                self.means[s] = np.random.rand(n_features)
                self.covs[s] = np.ones(n_features)

    def _gaussian_pdf(self, x, mean, cov):
        """
        Calculate Gaussian Probability Density Function manually.
        P(x) = (1 / sqrt((2pi)^k * det(Sigma))) * exp(-0.5 * (x-mu)T * Sigma^-1 * (x-mu))
        Using diag covariance for simplicity and speed.
        """
        n_features = len(x)
        # Log version to avoid underflow:
        # log P(x) = -0.5 * (k * log(2pi) + log(det(Sigma)) + (x-mu)^2 / Sigma)
        
        # Constant part
        log_2pi = np.log(2 * np.pi)
        
        # Check cov > 0
        cov = np.maximum(cov, 1e-5)
        
        log_det = np.sum(np.log(cov))
        
        diff = x - mean
        exponent = np.sum((diff ** 2) / cov)
        
        log_prob = -0.5 * (n_features * log_2pi + log_det + exponent)
        return log_prob

    def _calc_log_B(self, X):
        """
        Calculate Log Emission Probabilities: log B[t, j] = log P(O_t | State_j)
        """
        T = X.shape[0]
        log_B = np.zeros((T, self.n_states))
        
        for t in range(T):
            for s in range(self.n_states):
                log_B[t, s] = self._gaussian_pdf(X[t], self.means[s], self.covs[s])
        
        return log_B

    def _forward(self, log_B):
        """
        Forward Algorithm in Log Domain.
        alpha[t, j] = P(O_1...O_t, q_t=j | model)
        """
        T = log_B.shape[0]
        log_alpha = np.zeros((T, self.n_states))
        
        # Init t=0
        # alpha[0, i] = pi[i] * b_i(O_0)
        # log_alpha[0, i] = log(pi[i]) + log_b_i(O_0)
        with np.errstate(divide='ignore'):
            log_pi = np.log(self.pi)
            log_A = np.log(self.A)
            
        log_alpha[0] = log_pi + log_B[0]
        
        # Induction
        for t in range(1, T):
            for j in range(self.n_states):
                # Sum over i: alpha[t-1, i] * A[i, j]
                # LogSumExp trick: log(sum(exp(x)))
                # temp = log_alpha[t-1] + log_A[:, j]
                temp = log_alpha[t-1] + log_A[:, j]
                max_val = np.max(temp)
                log_sum = max_val + np.log(np.sum(np.exp(temp - max_val)))
                
                log_alpha[t, j] = log_sum + log_B[t, j]
                
        return log_alpha

    def _backward(self, log_B):
        """
        Backward Algorithm in Log Domain.
        beta[t, i] = P(O_t+1...O_T | q_t=i, model)
        """
        T = log_B.shape[0]
        log_beta = np.zeros((T, self.n_states))
        
        # Init t=T-1 (Last state) -> beta = 1 -> log_beta = 0
        log_beta[T-1] = 0.0
        
        with np.errstate(divide='ignore'):
            log_A = np.log(self.A)
            
        # Induction
        for t in range(T-2, -1, -1):
            for i in range(self.n_states):
                # Sum over j: A[i, j] * b_j(O_t+1) * beta[t+1, j]
                temp = log_A[i, :] + log_B[t+1, :] + log_beta[t+1, :]
                max_val = np.max(temp)
                log_sum = max_val + np.log(np.sum(np.exp(temp - max_val)))
                log_beta[t, i] = log_sum
                
        return log_beta

    def train(self, X):
        """
        Baum-Welch Training (EM Algorithm)
        X: List of observations or Single observation sequence?
        For this simplified/scratch version, let's assume One Sequence per call or loop over sequences. 
        Usually we average over multiple files.
        Here: X is a SINGLE sequence (n_samples, n_features) for simplicity, or we adapt to list.
        Adaptation: X is a LIST of arrays.
        """
        # If X is array, make it a list
        if isinstance(X, np.ndarray):
            X = [X]
            
        # Initialize if not already
        if self.means is None:
            # Concat all to init
            all_data = np.vstack(X)
            self._init_params(all_data)
            
        for it in range(self.n_iter):
            # Accumulators for A, means, covs
            # Expectation Step (E-Step)
            
            # Since we need to sum over multiple observations, we need careful accumulators
            # This is complex in "scratch" code.
            # Simplified approach: Train on 1 concatenated sequence? No, transitions are wrong.
            # Correct approach: Accumulate expectations.
            
            numer_A = np.zeros((self.n_states, self.n_states))
            denom_A = np.zeros((self.n_states, 1))
            
            numer_means = np.zeros((self.n_states, X[0].shape[1]))
            numer_covs = np.zeros((self.n_states, X[0].shape[1]))
            denom_gamma = np.zeros((self.n_states))
            
            for obs in X:
                log_B = self._calc_log_B(obs)
                log_alpha = self._forward(log_B)
                log_beta = self._backward(log_B)
                
                # Compute Gamma (State Probability)
                # gamma[t, i] = P(q_t = i | O, model) = alpha * beta / P(O)
                log_prob_O = np.max(log_alpha[-1]) # Or logsumexp of alpha[-1]
                # Better log_P_O:
                temp = log_alpha[-1]
                max_val = np.max(temp)
                log_P_O = max_val + np.log(np.sum(np.exp(temp - max_val)))
                
                log_gamma = log_alpha + log_beta - log_P_O
                gamma = np.exp(log_gamma)
                
                # Compute Xi (Transition Probability)
                # xi[t, i, j] = P(q_t=i, q_t+1=j | O, model)
                T = len(obs)
                log_A = np.log(self.A + 1e-10)
                
                # Accumulate for A
                for t in range(T-1):
                    # log_xi[t, i, j] = alpha[t,i] + A[i,j] + B[t+1,j] + beta[t+1,j] - log_P_O
                    for i in range(self.n_states):
                        for j in range(self.n_states):
                            log_xi_t_ij = log_alpha[t, i] + log_A[i, j] + log_B[t+1, j] + log_beta[t+1, j] - log_P_O
                            xi_t_ij = np.exp(log_xi_t_ij)
                            numer_A[i, j] += xi_t_ij
                    
                    denom_A += gamma[t].reshape(-1, 1)

                # Accumulate for Means/Covs
                # Sum gamma over time
                gamma_sum = np.sum(gamma, axis=0) # shape (n_states,)
                denom_gamma += gamma_sum
                
                for s in range(self.n_states):
                    # Weighted sum of observations
                    # obs: (T, D), gamma[:, s]: (T,)
                    w = gamma[:, s].reshape(-1, 1)
                    numer_means[s] += np.sum(obs * w, axis=0)
                    numer_covs[s] += np.sum((obs ** 2) * w, axis=0)
            
            # Maximization Step (M-Step)
            # Update A
            self.A = numer_A / (denom_A + 1e-10)
            # Normalize A
            self.A = self.A / np.sum(self.A, axis=1, keepdims=True)
            
            # Update Means
            self.means = numer_means / (denom_gamma[:, None] + 1e-10)
            
            # Update Covs (Diagonal)
            # var = E[x^2] - (E[x])^2
            # We calculated sum(w * x^2), so divide by sum(w) then subtract mean^2
            mean_sq = self.means ** 2
            avg_sq = numer_covs / (denom_gamma[:, None] + 1e-10)
            self.covs = avg_sq - mean_sq
            self.covs = np.maximum(self.covs, 1e-4) # Floor cov
            
            print(f"Iteration {it}: Params Updated")

    def score(self, observation):
        """
        Calculate Log-Likelihood of an observation sequence
        """
        log_B = self._calc_log_B(observation)
        log_alpha = self._forward(log_B)
        
        # log P(O) = log sum(alpha[T-1])
        temp = log_alpha[-1]
        max_val = np.max(temp)
        log_prob = max_val + np.log(np.sum(np.exp(temp - max_val)))
        return log_prob
