from app.best_sample import NumberSampling

sampling_instance = NumberSampling()
sampling_instance.set_sampling_data()

data = sampling_instance.power_set.copy()
data = sampling_instance.filtering_for_boundary(data)
data = sampling_instance.filtering_for_duplicated(data)
data = sampling_instance.filtering_for_continuous(data)
data = sampling_instance.filtering_for_combine(data)
data = sampling_instance.filtering_for_probability(data)
   
print(data)
