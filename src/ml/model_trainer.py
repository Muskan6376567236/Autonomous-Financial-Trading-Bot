import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import logging

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
    
    def prepare_data(self, df, sequence_length=60):
        """Prepare time series data for LSTM training"""
        try:
            # Get closing prices
            prices = df['close'].values.reshape(-1, 1)
            
            # Scale data
            scaled_prices = self.scaler.fit_transform(prices)
            
            # Create sequences
            X, y = [], []
            for i in range(sequence_length, len(scaled_prices)):
                X.append(scaled_prices[i-sequence_length:i, 0])
                y.append(scaled_prices[i, 0])
            
            X, y = np.array(X), np.array(y)
            X = np.reshape(X, (X.shape[0], X.shape[1], 1))
            
            return train_test_split(X, y, test_size=0.2, random_state=42)
        
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise
    
    def build_model(self, input_shape):
        """Build LSTM model for price prediction"""
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        self.model = model
        return model
    
    def train(self, X_train, y_train, epochs=50, batch_size=32):
        """Train the model"""
        try:
            if self.model is None:
                input_shape = (X_train.shape[1], X_train.shape[2])
                self.build_model(input_shape)
            
            history = self.model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=0.2,
                verbose=1
            )
            
            logger.info("Model training completed")
            return history
        
        except Exception as e:
            logger.error(f"Error during training: {str(e)}")
            raise
    
    def predict(self, X):
        """Make predictions"""
        try:
            if self.model is None:
                raise ValueError("Model not trained. Call train() first.")
            
            predictions = self.model.predict(X)
            return self.scaler.inverse_transform(predictions)
        
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise