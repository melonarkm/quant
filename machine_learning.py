from sklearn.ensemble import RandomForestClassifier


class MLStrategy(bt.Strategy):
    params = (
        ('training_period', 252),  # 1 year of training data
        ('retrain_freq', 21)  # Retrain monthly
    )

    def __init__(self):
        self.model = None
        self.last_retrain = 0
        self.features = [
            bt.indicators.RSI(period=14),
            bt.indicators.MACD(),
            bt.indicators.ATR(period=14)
        ]

    def next(self):
        # Retrain model periodically
        if len(self) - self.last_retrain >= self.p.retrain_freq:
            self.train_model()
            self.last_retrain = len(self)

        # Generate prediction
        X = np.array([f[0] for f in self.features]).reshape(1, -1)
        pred = self.model.predict(X)[0]

        # Execute trade
        if pred == 1:  # Buy signal
            self.order_target_percent(target=0.95)
        elif pred == -1:  # Sell signal
            self.order_target_percent(target=0.05)

    def train_model(self):
        # Prepare training data (simplified)
        X = np.random.randn(self.p.training_period, len(self.features))
        y = np.random.choice([-1, 0, 1], size=self.p.training_period)

        # Train Random Forest
        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(X, y)