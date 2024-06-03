
import numpy as np
import pandas as pd

from analysis.core_metric import MetricAnalysis

class NumberSampling(MetricAnalysis):
    
    sampling_n = 100000
    
    def __init__(self):
        
        super().__init__()
        
        self.update_db()
        self.set_data()
        self.set_metric_basic()
        
        self.boundary = self.get_boundary(interval=1)
        self.continuous_loc_weights = self.get_continuous_describe()
        self.combine_prob = self.get_side_combine_prob()[1]
        self.weights_matrix = self.get_weight()
        
    def set_sampling_data(self):
        
        power_set = np.zeros((self.sampling_n, 6), dtype=int)
        for try_n in range(self.sampling_n):
            sampling_vector = np.random.choice(range(1, 46), size=6, replace=False)
            power_set[try_n] = np.sort(sampling_vector)
        
        self.power_set = pd.DataFrame(power_set)
        return self.power_set
    
    def filtering_for_boundary(self, data: pd.DataFrame):
        
        input_dataset = data.copy()
        sample_mean = input_dataset.mean(axis=1)
        
        sample_idx = list()
        lower_bound, upper_bound = self.boundary
        
        for idx, value in enumerate(sample_mean.values):
            if (value >= lower_bound) and (value <= upper_bound):
                sample_idx.append(idx)
        
        boundaried_dataset = input_dataset.iloc[sample_idx].copy()
        return boundaried_dataset
    
    def filtering_for_duplicated(self, data: pd.DataFrame):
        
        input_dataset = data.copy()
        input_row_list = list()
        for idx, row in input_dataset.iterrows():
            input_row_list.append(tuple(row))
            
        winning_dataset = self.only_num_data.copy()
        winning_row_list = list()
        for idx, row in winning_dataset.iterrows():
            winning_row_list.append(tuple(row))
            
        input_set = set(input_row_list)
        winning_set = set(winning_row_list)
        
        differed_dataset = pd.DataFrame(input_set - winning_set)
        distincted_dataset = differed_dataset.drop_duplicates()
        
        return distincted_dataset        
        
    def filtering_for_continuous(self, data: pd.DataFrame):
        
        input_dataset = data.copy()
        input_loc_matrix = self.get_continuous_loc_matrix(input_dataset)
        input_loc_matrix['key'] = input_loc_matrix.apply(
            lambda row: ''.join(row.values.astype(str)), axis=1
        )
        weighted_sampling = input_loc_matrix.sample(
            n=len(self.data),
            weights=input_loc_matrix['key'].map(self.continuous_loc_weights)
        )
        sampled_index = weighted_sampling.index
        sampled_data = input_dataset.loc[sampled_index]        
        return sampled_data
    
    def filtering_for_combine(self, data: pd.DataFrame):
        
        input_dataset = data.copy()
        side_data = self.get_side_combine_prob(input_dataset)[0]
        weighted_sampling = side_data.sample(
            n=int(len(input_dataset)/2),
            weights=side_data['side'].map(self.combine_prob)
        )
        sampled_index = weighted_sampling.index
        sampled_data = input_dataset.loc[sampled_index]
        return sampled_data
    
    def filtering_for_probability(self, data: pd.DataFrame):
        
        input_dataset = data.copy()
        convert_target_data = input_dataset.copy()        
        convert_target_data = convert_target_data.astype(float)
        
        for col_idx, col in enumerate(convert_target_data):    
            col_name = self.weights_matrix.columns[col_idx]
            weights = self.weights_matrix[col_name]
            
            for order, value in enumerate(convert_target_data[col].values):
                row_idx = convert_target_data.index[order]
                convert_target_data.at[row_idx, col] = float(weights[value])
        
        middle_column = convert_target_data.columns[1:-1]    
        convert_target_data['prob'] = convert_target_data[middle_column].prod(axis=1)
        sorted_converted = convert_target_data.sort_values(by='prob', ascending=False)
        
        top_10 = sorted_converted.head(10).index
        selected_data = input_dataset.loc[top_10]
        
        return selected_data
        

if __name__ == '__main__':
    
    sampling_instance = NumberSampling()
    sampling_instance.set_sampling_data()
    
    data = sampling_instance.power_set.copy()
    data = sampling_instance.filtering_for_boundary(data)
    data = sampling_instance.filtering_for_duplicated(data)
    data = sampling_instance.filtering_for_continuous(data)
    data = sampling_instance.filtering_for_combine(data)
    data = sampling_instance.filtering_for_probability(data)
       
    
    