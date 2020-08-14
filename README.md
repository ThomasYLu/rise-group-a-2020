# Rise 2020 - Group A Repository
**Authors: Thomas Lu<sup>1,5</sup>, Aarohi Nadkarni<sup>2,5</sup>, Sophia Ma<sup>3,5</sup>, Sreeanvitha Emani<sup>4,5</sup>, Dr. Marianne Bezaire<sup>5</sup>**

## Description
This is the code repository for the project, "Decreased Calcium Concentrations Lead to Hyperexcitability in Computational Network Model of the Dentate Gyrus", conducted as part of Boston University's RISE program in the summer of 2020. Starting code is adapted from Santhakumar et al. (2005): https://senselab.med.yale.edu/ModelDB/ShowModel?model=51781#tabs-1
Our poster is located on our website: https://anviemani.github.io/rise-group-a-2020/

## Project Abstract
Seizures are a dangerous consequence of hyperexcitable neuronal networks in the brain and affect over 50 million epileptic patients around the world. Hypocalcemia (low blood calcium concentration) is one factor found to contribute to seizures, but this phenomenon is highly counterintuitive given calcium’s role in driving neuron firing. Additionally, hypocalcemia-induced seizures and their underlying mechanisms are still relatively underexplored in both experimental and computational settings. However, identifiable molecular mechanisms exist based on previous experimental observations, such as calcium interacting with leaky sodium channels (NALCN) and voltage-gated sodium channels (VGSC) to increase neuron excitability. We used a previously studied, 527-cell computational model of the dentate gyrus, a brain region in the hippocampus, to analyze network excitability due to lowered calcium concentrations. In particular, using experimental observations in the literature, we implemented code to relate external calcium to 1) NALCN conductance, and 2) VGSC voltage sensitivity. We then simulated the network under external calcium concentrations between 0.1 mM and 2.0 mM and generated analyses of network and neuron activity, including spike rasters and duration of network activity. Low calcium concentrations were found to have a significant enhancing effect on network excitability, which is consistent with the literature. Additionally, both models (VGSC and NALCN) saw an increase in excitability with decreasing calcium concentration, with the VGSC model's excitability increasing more rapidly. However, VGSC excitability greatly decreased for concentrations around 0.2 mM and below, while NALCN maintains excitability; we believe this provides an explanation for the experimental observation that only NALCN contributes to hypocalcemic excitability, as those evaluations were performed in relatively lower calcium concentrations. This study provides a first computational insight on mechanisms and dynamics of hypocalcemia-induced seizures. Future studies can build on our approach and findings to further understand the specific molecular mechanisms underlying this phenomenon.


### Affiliations
<sup>1</sup>Thomas Jefferson High School for Science and Technology, 6560 Braddock Rd, Alexandria, VA 22312
<sup>2</sup>Unionville High School, 750 Unionville Rd, Kennett Square, PA 19348
<sup>3</sup>Phillips Academy, 180 Main St, Andover, MA 01810
<sup>4</sup>Massachusetts Academy of Math and Science at WPI, 85 Prescott St, Worcester, MA 01605
<sup>5</sup>Boston University, Boston, MA 02215
