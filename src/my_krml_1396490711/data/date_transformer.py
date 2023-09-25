import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class DateFeaturesTransformer(BaseEstimator, TransformerMixin):
    def fit(self, clean_df, y=None):
        return self
    
    def transform(self, clean_df):
        clean_df_copy = clean_df.copy()
        clean_df_copy['date'] = pd.to_datetime(clean_df_copy['date'])
        clean_df_copy['weekday'] = clean_df_copy['date'].dt.weekday
        clean_df_copy['day'] = clean_df_copy['date'].dt.day
        clean_df_copy['week'] = clean_df_copy['date'].dt.strftime('%W')
        clean_df_copy['month'] = clean_df_copy['date'].dt.month
        
        # Convert to ordinal
        # ordinal_encoder = OrdinalEncoder()
        # date_features = ['weekday', 'day', 'week', 'month'] # Removed year from this list since this data is only 2012
        # ord_features = clean_df_copy[date_features].copy()  # Copy the date related features
        # ord_features_encoded = ordinal_encoder.fit_transform(ord_features)
        
        # Replace the original columns with the ordinal encoded values
        # clean_df_copy[date_features] = ord_features_encoded
        
        return clean_df_copy[['weekday', 'day', 'week', 'month']] # couldn't get ordinal encoding to work 