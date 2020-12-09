# BrainBrowser
### 소프트웨어융합캡스톤디자인(SWCON40100) 개인 프로젝트
##### 경희대학교 응용수학과/소프트웨어융합학과 박승혜
  
BrainBrowser는 Python의 Plotly Dash를 사용하여 제작한 Web-based visualize software로, 사용자와의 상호작용을 통해 즉각적인 시각화 결과물을 확인할 수 있습니다.   
  
## 시각화 결과물  

#### Intro Section
<img src="https://user-images.githubusercontent.com/50431248/101647748-70566d00-3a7c-11eb-8dee-86c62def1c2f.png" width="90%"></img>   
Intro Section에서는 두 개의 버튼과 상단의 네비게이션을 확인할 수 있습니다.   
네비게이션을 통해 원하는 위치로 바로 이동할 수 있습니다.    
* Basic Data 버튼을 클릭시 프로그램 자체에서 고유적으로 가지고 있는 파일을 사용하여 바로 툴을 사용해볼 수 있도록 Analysis section으로 연결됩니다.   
* Own Data 버튼을 클릭시 사용자가 가지고 있는 파일을 적용하여 툴을 사용해볼 수 있도록 파일을 업로드하는 Data Section으로 연결됩니다.  
Intro Section 아래에는 툴에 대한 설명이 짧게 들어가는 About Section이 등장합니다.   
   
#### Data Section
<img src="https://user-images.githubusercontent.com/50431248/101647456-1bb2f200-3a7c-11eb-80e7-b254edb4a6c7.png" width="90%"></img>   
Data Section에서는 세 종류의 파일을 업로드할 수 있습니다.   
* Structural MRI Data : Analysis와 Table, Graph Section에서 사용되는 데이터입니다. 데이터는 성별, 나이를 포함하여야 하며 Free-surfer으로 구분되는 66가지 뇌영역에 대한 thickness와 area 정보를 가져야합니다. 파일의 확장자는 csv이어야 합니다. 정확한 데이터 형식은 [이곳](https://github.com/con11235/BrainBrowser/blob/main/data/free_surfer_data2.csv)에서 확인하세요.(위에서 언급한 정보 외의 정보는 없어도 무관합니다.)
<details>
  <summary>필수 데이터 열 명칭 확인하기</summary>
  
  - Age : 나이
  - Sex : 성별
  - BrainSeg_Vol : 전체 부피  
      
   **Free-Surfer** : 이하 모든 구역들은 명칭 앞에 L_ 또는 R_을 붙여 좌우를 구분하고, 명칭 뒤에 Thck와 Area를 붙여 사용합니다.
  - Bankssts
  - Caudalanteriorcingulate
  - Caudalmiddlefrontal
  - Cuneus
  - Entorhinal
  - Fusiform
  - Inferiorparietal
  - Inferiortemporal
  - Isthmuscingulate
  - Lateraloccipital
  - Lateralorbitofrontal
  - Lingual
  - Medialorbitofrontal
  - Middletemporal
  - Parahippocampal
  - Paracentral
  - Parsopercularis
  - Parsorbitalis
  - Parstriangularis
  - Pericalcarine
  - Postcentral
  - Posteriorcingulate
  - Precentral
  - Precuneus
  - Rostralanteriorcingulate
  - Rostralmiddlefrontal
  - Superiorfrontal
  - Superiorparietal
  - Superiortemporal
  - Supramarginal
  - Frontalpole
  - Temporalpole
  - Transversetemporal
  - Insula
</details>

* Atlas Data : 3D Brain viewer의 표면에 나타낼 정보를 의미합니다. 66가지의 Free-surfer 영역마다 하나의 정수 값을 가지며, 이는 txt 파일에 한 줄에 하나의 정수씩 총 66줄이 입력되어있어야 합니다. 정확한 데이터 형식은 [이곳](https://github.com/con11235/BrainBrowser/blob/main/data/atlas_test.txt)에서 확인하세요.  
* Brain Connectivity Data : Connectivity Section에 나타낼 정보를 의미합니다. (66,66) shape의 행렬 데이터를 갖는 csv파일이며, 각 행/열에 해당하는 영역간의 연관성 값을 갖도록 합니다. Header는 갖지 않습니다. 정확한 데이터 형식은 [이곳](https://github.com/con11235/BrainBrowser/blob/main/data/connectivity_test.csv)에서 확인하세요.

<details>
  <summary>데이터 순서 확인하기(Atlas와 Brain Connectivity는 같은 데이터 순서를 가집니다.)</summary>

[참고](https://github.com/con11235/BrainBrowser/blob/main/data/Hagmann_66regions.CSV)  
1. Bank of the superior temporal sulcus
2. Caudal anterior cingulate cortex
3. Caudal middle frontal cortex
4. Cuneus
5. Entorhinial cortex
6. Frontal pole
7. Fusiform gyrus
8. Inferior parietal cortex
9. Inferior temporal cortex
10. Isthmus of the cingulate cortex
11. Lateral occipital cortex
12. Lateral orbitofrontal cortex
13. Lingual gyrus
14. Medial orbitofrontal cortex
15. Middle temporal cortex
16. Paracentral lobule
17. Parahippocampal cortex
18. Pars opercularis
19. Pars orbitalis
20. Pars triangularis
21. Pericalcarine cortex
22. Postcentral gyrus
23. Posterior cingulate cortex
24. Precentral gyrus
25. Precuneus
26. Rostral anterior cingulate cortex
27. Rostral middle frontal cortex
28. Superior frontal cortex
29. Superior parietal cortex
30. Superior temporal cortex
31. Supramarginal gyrus
32. Temporal pole
33. Transverse temporal cortex
34. Bank of the superior temporal sulcus
35. Caudal anterior cingulate cortex
36. Caudal middle frontal cortex
37. Cuneus
38. Entorhinial cortex
39. Frontal pole
40. Fusiform gyrus
41. Inferior parietal cortex
42. Inferior temporal cortex
43. Isthmus of the cingulate cortex
44. Lateral occipital cortex
45. Lateral orbitofrontal cortex
46. Lingual gyrus
47. Medial orbitofrontal cortex
48. Middle temporal cortex
49. Paracentral lobule
50. Parahippocampal cortex
51. Pars opercularis
52. Pars orbitalis
53. Pars triangularis
54. Pericalcarine cortex
55. Postcentral gyrus
56. Posterior cingulate cortex
57. Precentral gyrus
58. Precuneus
59. Rostral anterior cingulate cortex
60. Rostral middle frontal cortex
61. Superior frontal cortex
62. Superior parietal cortex
63. Superior temporal cortex
64. Supramarginal gyrus
65. Temporal pole
66. Transverse temporal cortex
</details>

### Analysis Section
<img src="https://user-images.githubusercontent.com/50431248/101647459-1bb2f200-3a7c-11eb-85f0-cbdcdbfa3005.png" width="90%"></img>
<img src="https://user-images.githubusercontent.com/50431248/101647462-1c4b8880-3a7c-11eb-98ab-4be82497b250.png" width="90%"></img>
Analysis Section에서는 Thickness data에 대한 정보를 모듈별로 보여줍니다. dropdown을 사용하여 Box와 Violin 중 원하는 그래프를 선택할 수 있습니다.  
필요에 따라 원하는 성별만을 선택하여 확인할 수 있습니다. 그래프 위에 마우스를 올리면 구체적인 정보를 알 수 있습니다.
<details>
  <summary>모듈 정보</summary>
  
  각 영역의 축약명에 대한 정보는 [이곳](https://github.com/con11235/BrainBrowser/blob/main/data/Hagmann_66regions.CSV)에서 참고하세요. 
  1. lCUN, lLING, lPARH, lPCAL, lPCUN, rCUN, rLING, rPCAL
  2. lCAC, lISTC, lPARC, lPC, rCAC, rISTC, rPARC, rPC, rPCUN
  3. lBSTS, lENT, lFUS, lIP, lIT, lLOCC, lMT, lPSTC, lSP, lST, lSMAR, lTP, lTT
  4. rBSTS, rENT, rFUS, rIP, rIT, rLOCC, rMT, rPARH, rPSTC, rSP, rST, rSMAR, rTP, rTT
  5. lCMF, lFP, lLOF, lMOF, lPOPE, lPORB, lPTRI, lPREC, lRAC, lRMF, lSF
  6. rCMF, rFP, rLOF, rMOF, rPOPE, rPORB, rPTRI, rPREC, rRAC, rRMF, rSF
</details>


### 3D Brain Section
<img src="https://user-images.githubusercontent.com/50431248/101647464-1c4b8880-3a7c-11eb-8f91-d5d24972815d.png" width="90%"></img>
3D Brain Section에서는 뇌의 표면을 시각화하여 보여줍니다. 표면을 클릭하면 클릭한 영역에 대한 정보를 아래의 Table, Graph, Connectivity에서 표시합니다.
위 시각화 방법은 [BrainBrowser - MCGILL CENTRE for INTEGRATIVE NEUROSCIENCE](https://mcin.ca/technology/visualization/brainbrowser/)에서 참고하여 구현하였습니다.

## Table Section
<img src="https://user-images.githubusercontent.com/50431248/101647468-1ce41f00-3a7c-11eb-9cbe-b12a52b69726.png" width="90%"></img>
Table Section에서는 클릭한 위치 좌표와 해당 영역의 명칭을 알려줍니다. 클릭한 위치의 데이터들에 대한 수치적인 정보와, 그 아래에 모든 data들을 보여줍니다.

## Graph Section
<img src="https://user-images.githubusercontent.com/50431248/101647471-1d7cb580-3a7c-11eb-8cd0-834d72482e2b.png" width="90%"></img>
Graph Section에서는 Table에서 보여준 data들을 plot하여 보여줍니다. 여기서는 나이에 따른 정보를 확인할 수 있으며, 나이에 따른 회귀곡선도 함께 표현됩니다.  
Plot의 종류는 Dropdown을 통해 scatter와 Box 중에서 선택할 수 있습니다.

## Connectivity Section
<img src="https://user-images.githubusercontent.com/50431248/101647473-1e154c00-3a7c-11eb-80b7-21911bc69758.png" width="90%"></img>
Circos 그래프는 클릭된 영역과 연관된 연결선들을 표시해줍니다. 안쪽 원 위에 커서를 올리면 해당 영역의 명칭을 확인할 수 있습니다.
<img src="https://user-images.githubusercontent.com/50431248/101647478-1eade280-3a7c-11eb-8a9e-9be79f809c05.png" width="90%"></img>
3D connectivity는 마찬가지로 선택된 영역과 그에 연결된 연결선들을 표시해줍니다.


## 사용 방법
1. 파일을 다운받아 다음과 같은 폴더 구성을 만듭니다.
ProjectFolder
├─ assets
│  ├─ img
│  │   ├─ about-bg.jpg
│  │   ├─ intro-bg.jpg
│  │   └─ logo.png
│  ├─ bootstrap-grid.css
│  ├─ favicon.ico
│  ├─ main.js
│  └─ style.css
├─ data
│  ├─ connectivity.csv
│  ├─ connectivity.mat
│  ├─ free_surfer_data.csv
│  ├─ fs-atlas.txt
│  ├─ Hagmann_66regions.xlsx
│  └─ human_brain.obj
├─ app.py
├─ datas.py
├─ index.py
└─ utils.py
.py 외의 파일들은 없어도 무관합니다.

2. CMD 또는 PowerShell 등에서 index.py를 실행시킵니다.
```
cd (index파일 directory)
python index.py
```

3. [127.0.0.1:8050/](http://127.0.0.1:8050/)에서 실행 결과물을 확인할 수 있습니다.

## 필요한 모듈 및 사용한 버전
* dash==1.16.1
* dash-bio==0.4.8
* dash-bio-utils==0.0.5
* dash-bootstrap-components==0.10.7
* dash-colorscales==0.0.4
* dash-core-components==1.12.1
* dash-html-components==1.1.1
* dash-renderer==1.8.1
* dash-table==4.10.1
* numpy==1.18.3
* pandas==1.0.3
* plotly==4.9.0


## 참고자료
* [Plotly-Dash](https://dash.plotly.com/)
* [Dash Core Components](https://dash.plotly.com/dash-core-components)
* [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/quickstart/)
* [Dash Sample Apps](https://github.com/plotly/dash-sample-apps)
* [BrainBrowser - MCIN](https://mcin.ca/technology/visualization/brainbrowser/)
* [참고한 웹 디자인 소스](https://bootstrapmade.com/theevent-conference-event-bootstrap-template/)
