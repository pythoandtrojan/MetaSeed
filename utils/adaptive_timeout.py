class AdaptiveTimeout:
    def __init__(self, initial_timeout=5, max_timeout=30):
        self.timeout = initial_timeout
        self.max_timeout = max_timeout
        self.success_count = 0
        self.failure_count = 0
        
    def update_timeout(self, success):
        if success:
            self.success_count += 1
            self.failure_count = max(0, self.failure_count - 1)
            # Reduzir timeout gradualmente se houver sucesso
            if self.success_count > 3:
                self.timeout = max(1, self.timeout * 0.9)
                self.success_count = 0
        else:
            self.failure_count += 1
            self.success_count = 0
            # Aumentar timeout se houver falhas
            if self.failure_count > 2:
                self.timeout = min(self.max_timeout, self.timeout * 1.5)
                
    def get_timeout(self):
        return self.timeout
        
    def reset(self):
        self.timeout = 5
        self.success_count = 0
        self.failure_count = 0
