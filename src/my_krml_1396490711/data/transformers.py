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
    

events_data = [
    ['2011-02-06', 'SuperBowl', 'Sporting'],
    ['2011-02-14', 'ValentinesDay', 'Cultural'],
    ['2011-02-21', 'PresidentsDay', 'National'],
    ['2011-03-09', 'LentStart', 'Religious'],
    ['2011-03-16', 'LentWeek2', 'Religious'],
    ['2011-03-17', 'StPatricksDay', 'Cultural'],
    ['2011-03-20', 'Purim End', 'Religious'],
    ['2011-04-24', 'Easter', 'Cultural'],
    ['2011-04-24', 'OrthodoxEaster', 'Religious'],
    ['2011-04-26', 'Pesach End', 'Religious'],
    ['2011-05-05', 'Cinco De Mayo', 'Cultural'],
    ['2011-05-08', "Mother's day", 'Cultural'],
    ['2011-05-30', 'MemorialDay', 'National'],
    ['2011-05-31', 'NBAFinalsStart', 'Sporting'],
    ['2011-06-12', 'NBAFinalsEnd', 'Sporting'],
    ['2011-06-19', "Father's day", 'Cultural'],
    ['2011-07-04', 'IndependenceDay', 'National'],
    ['2011-08-01', 'Ramadan starts', 'Religious'],
    ['2011-08-31', 'Eid al-Fitr', 'Religious'],
    ['2011-09-05', 'LaborDay', 'National'],
    ['2011-10-10', 'ColumbusDay', 'National'],
    ['2011-10-31', 'Halloween', 'Cultural'],
    ['2011-11-07', 'EidAlAdha', 'Religious'],
    ['2011-11-11', 'VeteransDay', 'National'],
    ['2011-11-24', 'Thanksgiving', 'National'],
    ['2011-12-25', 'Christmas', 'National'],
    ['2011-12-28', 'Chanukah End', 'Religious'],
    ['2012-01-01', 'NewYear', 'National'],
    ['2012-01-07', 'OrthodoxChristmas', 'Religious'],
    ['2012-01-16', 'MartinLutherKingDay', 'National'],
    ['2012-02-05', 'SuperBowl', 'Sporting'],
    ['2012-02-14', 'ValentinesDay', 'Cultural'],
    ['2012-02-20', 'PresidentsDay', 'National'],
    ['2012-02-22', 'LentStart', 'Religious'],
    ['2012-02-29', 'LentWeek2', 'Religious'],
    ['2012-03-08', 'Purim End', 'Religious'],
    ['2012-03-17', 'StPatricksDay', 'Cultural'],
    ['2012-04-08', 'Easter', 'Cultural'],
    ['2012-04-14', 'Pesach End', 'Religious'],
    ['2012-04-15', 'OrthodoxEaster', 'Religious'],
    ['2012-05-05', 'Cinco De Mayo', 'Cultural'],
    ['2012-05-13', "Mother's day", 'Cultural'],
    ['2012-05-28', 'MemorialDay', 'National'],
    ['2012-06-12', 'NBAFinalsStart', 'Sporting'],
    ['2012-06-17', "Father's day", 'Cultural'],
    ['2012-06-21', 'NBAFinalsEnd', 'Sporting'],
    ['2012-07-04', 'IndependenceDay', 'National'],
    ['2012-07-20', 'Ramadan starts', 'Religious'],
    ['2012-08-19', 'Eid al-Fitr', 'Religious'],
    ['2012-09-03', 'LaborDay', 'National'],
    ['2012-10-08', 'ColumbusDay', 'National'],
    ['2012-10-26', 'EidAlAdha', 'Religious'],
    ['2012-10-31', 'Halloween', 'Cultural'],
    ['2012-11-11', 'VeteransDay', 'National'],
    ['2012-11-22', 'Thanksgiving', 'National'],
    ['2012-12-16', 'Chanukah End', 'Religious'],
    ['2012-12-25', 'Christmas', 'National'],
    ['2013-01-01', 'NewYear', 'National'],
    ['2013-01-07', 'OrthodoxChristmas', 'Religious'],
    ['2013-01-21', 'MartinLutherKingDay', 'National'],
    ['2013-02-03', 'SuperBowl', 'Sporting'],
    ['2013-02-13', 'LentStart', 'Religious'],
    ['2013-02-14', 'ValentinesDay', 'Cultural'],
    ['2013-02-18', 'PresidentsDay', 'National'],
    ['2013-02-20', 'LentWeek2', 'Religious'],
    ['2013-02-24', 'Purim End', 'Religious'],
    ['2013-03-17', 'StPatricksDay', 'Cultural'],
    ['2013-03-31', 'Easter', 'Cultural'],
    ['2013-04-02', 'Pesach End', 'Religious'],
    ['2013-05-05', 'Cinco De Mayo', 'Cultural'],
    ['2013-05-05', 'OrthodoxEaster', 'Religious'],
    ['2013-05-12', "Mother's day", 'Cultural'],
    ['2013-05-27', 'MemorialDay', 'National'],
    ['2013-06-06', 'NBAFinalsStart', 'Sporting'],
    ['2013-06-16', "Father's day", 'Cultural'],
    ['2013-06-20', 'NBAFinalsEnd', 'Sporting'],
    ['2013-07-04', 'IndependenceDay', 'National'],
    ['2013-07-09', 'Ramadan starts', 'Religious'],
    ['2013-08-08', 'Eid al-Fitr', 'Religious'],
    ['2013-09-02', 'LaborDay', 'National'],
    ['2013-10-14', 'ColumbusDay', 'National'],
    ['2013-10-15', 'EidAlAdha', 'Religious'],
    ['2013-10-31', 'Halloween', 'Cultural'],
    ['2013-11-11', 'VeteransDay', 'National'],
    ['2013-11-28', 'Thanksgiving', 'National'],
    ['2013-12-05', 'Chanukah End', 'Religious'],
    ['2013-12-25', 'Christmas', 'National'],
    ['2014-01-01', 'NewYear', 'National'],
    ['2014-01-07', 'OrthodoxChristmas', 'Religious'],
    ['2014-01-20', 'MartinLutherKingDay', 'National'],
    ['2014-02-02', 'SuperBowl', 'Sporting'],
    ['2014-02-14', 'ValentinesDay', 'Cultural'],
    ['2014-02-17', 'PresidentsDay', 'National'],
    ['2014-03-05', 'LentStart', 'Religious'],
    ['2014-03-12', 'LentWeek2', 'Religious'],
    ['2014-03-16', 'Purim End', 'Religious'],
    ['2014-03-17', 'StPatricksDay', 'Cultural'],
    ['2014-04-20', 'Easter', 'Cultural'],
    ['2014-04-20', 'OrthodoxEaster', 'Religious'],
    ['2014-04-22', 'Pesach End', 'Religious'],
    ['2014-05-05', 'Cinco De Mayo', 'Cultural'],
    ['2014-05-11', "Mother's day", 'Cultural'],
    ['2014-05-26', 'MemorialDay', 'National'],
    ['2014-06-05', 'NBAFinalsStart', 'Sporting'],
    ['2014-06-15', "Father's day", 'Cultural'],
    ['2014-06-15', 'NBAFinalsEnd', 'Sporting'],
    ['2014-06-29', 'Ramadan starts', 'Religious'],
    ['2014-07-04', 'IndependenceDay', 'National'],
    ['2014-07-29', 'Eid al-Fitr', 'Religious'],
    ['2014-09-01', 'LaborDay', 'National'],
    ['2014-10-04', 'EidAlAdha', 'Religious'],
    ['2014-10-13', 'ColumbusDay', 'National'],
    ['2014-10-31', 'Halloween', 'Cultural'],
    ['2014-11-11', 'VeteransDay', 'National'],
    ['2014-11-27', 'Thanksgiving', 'National'],
    ['2014-12-24', 'Chanukah End', 'Religious'],
    ['2014-12-25', 'Christmas', 'National'],
    ['2015-01-01', 'NewYear', 'National'],
    ['2015-01-07', 'OrthodoxChristmas', 'Religious'],
    ['2015-01-19', 'MartinLutherKingDay', 'National'],
    ['2015-02-01', 'SuperBowl', 'Sporting'],
    ['2015-02-14', 'ValentinesDay', 'Cultural'],
    ['2015-02-16', 'PresidentsDay', 'National'],
    ['2015-02-18', 'LentStart', 'Religious'],
    ['2015-02-25', 'LentWeek2', 'Religious'],
    ['2015-03-05', 'Purim End', 'Religious'],
    ['2015-03-17', 'StPatricksDay', 'Cultural'],
    ['2015-04-05', 'Easter', 'Cultural'],
    ['2015-04-11', 'Pesach End', 'Religious'],
    ['2015-04-12', 'OrthodoxEaster', 'Religious'],
    ['2015-05-05', 'Cinco De Mayo', 'Cultural'],
    ['2015-05-10', "Mother's day", 'Cultural'],
    ['2015-05-25', 'MemorialDay', 'National'],
    ['2015-06-04', 'NBAFinalsStart', 'Sporting'],
    ['2015-06-16', 'NBAFinalsEnd', 'Sporting'],
    ['2015-06-18', 'Ramadan starts', 'Religious'],
    ['2015-06-21', "Father's day", 'Cultural'],
    ['2015-07-04', 'IndependenceDay', 'National'],
    ['2015-07-18', 'Eid al-Fitr', 'Religious'],
    ['2015-09-07', 'LaborDay', 'National'],
    ['2015-09-24', 'EidAlAdha', 'Religious'],
    ['2015-10-12', 'ColumbusDay', 'National'],
    ['2015-10-31', 'Halloween', 'Cultural'],
    ['2015-11-11', 'VeteransDay', 'National'],
    ['2015-11-26', 'Thanksgiving', 'National'],
    ['2015-12-14', 'Chanukah End', 'Religious'],
    ['2015-12-25', 'Christmas', 'National'],
    ['2016-01-01', 'NewYear', 'National'],
    ['2016-01-07', 'OrthodoxChristmas', 'Religious'],
    ['2016-01-18', 'MartinLutherKingDay', 'National'],
    ['2016-02-07', 'SuperBowl', 'Sporting'],
    ['2016-02-10', 'LentStart', 'Religious'],
    ['2016-02-14', 'ValentinesDay', 'Cultural'],
    ['2016-02-15', 'PresidentsDay', 'National'],
    ['2016-02-17', 'LentWeek2', 'Religious'],
    ['2016-03-17', 'StPatricksDay', 'Cultural'],
    ['2016-03-24', 'Purim End', 'Religious'],
    ['2016-03-27', 'Easter', 'Cultural'],
    ['2016-04-30', 'Pesach End', 'Religious'],
    ['2016-05-01', 'OrthodoxEaster', 'Religious'],
    ['2016-05-05', 'Cinco De Mayo', 'Cultural'],
    ['2016-05-08', "Mother's day", 'Cultural'],
    ['2016-05-30', 'MemorialDay', 'National'],
    ['2016-06-02', 'NBAFinalsStart', 'Sporting'],
    ['2016-06-07', 'Ramadan starts', 'Religious'],
    ['2016-06-19', "Father's day", 'Cultural'],
    ['2016-06-19', 'NBAFinalsEnd', 'Sporting']]

# Define the column names
columns = ["date", "event_name", "event_type"]

# Create the DataFrame
eve_df = pd.DataFrame(events_data, columns=columns)


class EventTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, eve_df):
        self.eve_df = eve_df
    
    def fit(self, clean_df, y=None):
        return self
    
    def transform(self, clean_df):
        clean_df_copy = clean_df.merge(self.eve_df, on='date', how='left')
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
