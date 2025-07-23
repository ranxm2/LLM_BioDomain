import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# DeepSeek data
deepseek_csv = """precision@1,precision@2,recall@1,recall@2,method
0.8370247323735696,0.4673311184939092,0.8370247323735696,0.9346622369878184,DeepSeek_01-Name_Temp_0
0.8357327427094869,0.46936138796603916,0.8357327427094869,0.9387227759320783,DeepSeek_01-Name_Temp_0.1
0.841454411221853,0.4673311184939092,0.841454411221853,0.9346622369878184,DeepSeek_01-Name_Temp_0.5
0.8368401624215578,0.4666851236618679,0.8368401624215578,0.9333702473237357,DeepSeek_01-Name_Unknown_0
0.840531561461794,0.46806939830195643,0.840531561461794,0.9361387966039129,DeepSeek_01-Name_Temp_0.9
0.8359173126614987,0.45782576596530083,0.8359173126614987,0.9156515319306017,DeepSeek_02-Name_structure_Temp_0
0.8335179032853451,0.4603174603174603,0.8335179032853451,0.9206349206349206,DeepSeek_02-Name_structure_Unknown_0
0.8351790328534514,0.45930232558139533,0.8351790328534514,0.9186046511627907,DeepSeek_02-Name_structure_Temp_0.9
0.8337024732373569,0.4581949058693245,0.8337024732373569,0.916389811738649,DeepSeek_02-Name_structure_Temp_0.5
0.834625322997416,0.4590254706533776,0.834625322997416,0.9180509413067552,DeepSeek_02-Name_structure_Temp_0.1
0.804171280915467,0.4377076411960133,0.804171280915467,0.8754152823920266,DeepSeek_03-Name_structure_similarity_Temp_0.0
0.8015873015873016,0.4391842008121078,0.8015873015873016,0.8783684016242156,DeepSeek_03-Name_structure_similarity_Temp_0.1
0.8019564414913252,0.4367847914359542,0.8019564414913252,0.8735695828719084,DeepSeek_03-Name_structure_similarity_Temp_0.5
0.799187892211148,0.43549280177187155,0.799187892211148,0.8709856035437431,DeepSeek_03-Name_structure_similarity_Temp_0.9
0.7990033222591362,0.43899963086009597,0.7990033222591362,0.8779992617201919,DeepSeek_03-Name_structure_similarity_Unknown_Temp_0.0
0.7713178294573644,0.4421373200442968,0.7713178294573644,0.8842746400885936,DeepSeek_04-AD_temp_Temp_0.0
0.7703949796973053,0.4422296050203027,0.7703949796973053,0.8844592100406053,DeepSeek_04-AD_temp_Temp_0.1
0.7744555186415651,0.44370616463639717,0.7744555186415651,0.8874123292727943,DeepSeek_04-AD_temp_Temp_0.9
0.7722406792174235,0.44250645994832044,0.7722406792174235,0.8850129198966409,DeepSeek_04-AD_temp_Temp_0.5
0.7787006275378369,0.4425987449243263,0.7787006275378369,0.8851974898486527,DeepSeek_04-AD_temp_Unknown_Temp_0.0
"""
df_ds = pd.read_csv(StringIO(deepseek_csv)).set_index('method')

# Baseline and ChatGPT data
data = {
    'Random':                   [0.0553, 0.0553, 0.0533, 0.1063],
    'EditDist':                 [0.0855, 0.0725, 0.0826, 0.1397],
    'Graph Traversal':          [0.2102, 0.1289, 0.2037, 0.2495],
    'ChatGPT: GO name (0.0)':   [0.7780, 0.4377, 0.7780, 0.8754],
    'ChatGPT: GO name (0.1)':   [0.7788, 0.4378, 0.7788, 0.8757],
    'ChatGPT: GO name (0.5)':   [0.7746, 0.4357, 0.7746, 0.8715],
    'ChatGPT: GO name (0.9)':   [0.7641, 0.4305, 0.7641, 0.8610],
    'ChatGPT: allow Unknown (0.0)': [0.7237, 0.4160, 0.7236, 0.8320],
    'ChatGPT: GO structure (0.0)':  [0.7283, 0.4006, 0.7283, 0.8012],
    'ChatGPT: GO structure (0.1)':  [0.7264, 0.4005, 0.7264, 0.8010],
    'ChatGPT: GO structure (0.5)':  [0.7259, 0.3974, 0.7259, 0.7949],
    'ChatGPT: GO structure (0.9)':  [0.7153, 0.3934, 0.7153, 0.7868],
    'ChatGPT: allow Unknown structure': [0.7078, 0.4003, 0.7078, 0.8006],
    'ChatGPT: structure similarity (0.0)': [0.7211, 0.3875, 0.7211, 0.7750],
    'ChatGPT: structure similarity (0.1)': [0.7166, 0.3883, 0.7166, 0.7766],
    'ChatGPT: structure similarity (0.5)': [0.7122, 0.3883, 0.7166, 0.7766],
    'ChatGPT: structure similarity (0.9)': [0.7065, 0.3818, 0.7065, 0.7638],
    'ChatGPT: allow Unknown similarity': [0.7124, 0.3858, 0.7122, 0.7716],
    'ChatGPT: AD condition (0.0)': [0.7545, 0.4049, 0.7545, 0.8097],
    'ChatGPT: AD condition (0.1)': [0.7543, 0.4050, 0.7543, 0.8101],
    'ChatGPT: AD condition (0.5)': [0.7470, 0.4033, 0.7470, 0.8066],
    'ChatGPT: AD condition (0.9)': [0.7438, 0.4025, 0.7438, 0.8049],
    'ChatGPT: allow Unknown AD':   [0.6912, 0.4029, 0.6912, 0.8058],
}
df_other = pd.DataFrame.from_dict(data, orient='index',
                                columns=['precision@1','precision@2','recall@1','recall@2'])

# Combine all
df_all = pd.concat([df_other, df_ds])

# Split metrics
precision = df_all[['precision@1','precision@2']]
recall    = df_all[['recall@1','recall@2']]

# Plot side-by-side heatmaps with annotations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 14))

# Precision heatmap
im1 = ax1.imshow(precision.values, aspect='auto', cmap='viridis')
ax1.set_title('Precision Metrics (All Models)')
ax1.set_xticks(range(precision.shape[1]))
ax1.set_xticklabels(precision.columns, rotation=45, ha='right')
ax1.set_yticks(range(len(precision.index)))
ax1.set_yticklabels(precision.index)
for i in range(precision.shape[0]):
    for j in range(precision.shape[1]):
        ax1.text(j, i, f"{precision.values[i, j]:.2f}", ha='center', va='center', color='black')
fig.colorbar(im1, ax=ax1, orientation='vertical', label='Precision')

# Recall heatmap
im2 = ax2.imshow(recall.values, aspect='auto', cmap='plasma')
ax2.set_title('Recall Metrics (All Models)')
ax2.set_xticks(range(recall.shape[1]))
ax2.set_xticklabels(recall.columns, rotation=45, ha='right')
ax2.set_yticks(range(len(recall.index)))
ax2.set_yticklabels(recall.index)
for i in range(recall.shape[0]):
    for j in range(recall.shape[1]):
        ax2.text(j, i, f"{recall.values[i, j]:.2f}", ha='center', va='center', color='black')
fig.colorbar(im2, ax=ax2, orientation='vertical', label='Recall')

plt.tight_layout()


# save the figure to pdf
plt.savefig('summary_0715.pdf', format='pdf', bbox_inches='tight')
plt.close(fig)