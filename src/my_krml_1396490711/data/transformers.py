import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import pkg_resources

class DateFeaturesTransformer(BaseEstimator, TransformerMixin):
    def fit(self, clean_df, y=None):
        return self
    
    def transform(self, clean_df):
        clean_df_copy = clean_df.copy()
        clean_df_copy['date'] = pd.to_datetime(clean_df_copy['date'])
        clean_df_copy['weekday'] = clean_df_copy['date'].dt.weekday.astype(int)
        clean_df_copy['day'] = clean_df_copy['date'].dt.day.astype(int)
        clean_df_copy['week'] = clean_df_copy['date'].dt.strftime('%W').astype(int)
        clean_df_copy['month'] = clean_df_copy['date'].dt.month.astype(int)
        clean_df_copy['year'] = clean_df_copy['date'].dt.year.astype(int)
        
        # Convert to ordinal
        # ordinal_encoder = OrdinalEncoder()
        # date_features = ['weekday', 'day', 'week', 'month'] # Removed year from this list since this data is only 2012
        # ord_features = clean_df_copy[date_features].copy()  # Copy the date related features
        # ord_features_encoded = ordinal_encoder.fit_transform(ord_features)
        
        # Replace the original columns with the ordinal encoded values
        # clean_df_copy[date_features] = ord_features_encoded
        
        return clean_df_copy[['weekday', 'day', 'week', 'month', 'year']] # couldn't get ordinal encoding to work 
    

class ItemIdTransformer(BaseEstimator, TransformerMixin):
    def fit(self, clean_df, y=None):
        return self
    
    def transform(self, clean_df):
        clean_df_copy = clean_df.copy()
        clean_df_copy['transformed_item_id'] = clean_df_copy['item_id'].str.extract('_(\d+)$').astype(str)
        
        # One-hot encode 'transformed_item_id' using pd.get_dummies
        one_hot_encoded = pd.get_dummies(clean_df_copy['transformed_item_id'], prefix='item_id', dtype=int)
        
        # Concatenate the one-hot encoded columns with the original DataFrame
        transformed_df = pd.concat([clean_df_copy, one_hot_encoded], axis=1)
        
        # Drop the original 'transformed_item_id' column
        transformed_df.drop(['transformed_item_id', 'item_id'], axis=1, inplace=True)
        
        return transformed_df
    

class EventTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        # Load eve_df from the package's data directory
        data_file = pkg_resources.resource_filename(__name__, 'datasets/calendar_events.csv')
        self.calendar_events_df = pd.read_csv(data_file)
    
    def fit(self, clean_df, y=None):
        return self
    
    def transform(self, clean_df):
        clean_df_copy = clean_df.merge(self.calendar_events_df, on='date', how='left')
        clean_df_copy['event_name'].fillna('NoEvent', inplace=True)
        clean_df_copy['event_type'].fillna('NoEvent', inplace=True)
        
        # One-hot encode 'event_name' and 'event_type'
        event_name_encoded = pd.get_dummies(clean_df_copy['event_name'], prefix='event_name', dtype=int)
        event_type_encoded = pd.get_dummies(clean_df_copy['event_type'], prefix='event_type', dtype=int)
        
        # Concatenate the one-hot encoded columns with the original DataFrame
        transformed_df = pd.concat([clean_df_copy, event_name_encoded, event_type_encoded], axis=1)
        
        # Drop the original 'date', 'event_name' and 'event_type' columns
        transformed_df.drop(['date', 'event_name', 'event_type'], axis=1, inplace=True)
        
        return transformed_df
        
        #return clean_df_copy[['event_name', 'event_type']]
