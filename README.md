# PoliNetExtraction-App
A demo application for the automatic extraction of a policy network. The strength of relationships between the actors of the network are predicted from the semantic relatedness to the Jaccard, DICE and MI (Mutual Information) page-count metrics. This application is part of my master thesis which is also published in the 

T. Moschopoulos, E. Iosif, L. Demetropoulou, A. Potamianos and S. S. Narayanan, "Toward the Automatic Extraction of Policy Networks Using Web Links and Documents," in IEEE Transactions on Knowledge and Data Engineering, vol. 25, no. 10, pp. 2404-2417, Oct. 2013, doi: 10.1109/TKDE.2012.159.

The source code of the application consists of the following files:

1) front_end.py:       Which is the UI of the application buit in python
2) create_graph.pl:    Perl script for the creation of social network visualization graph
3) find_page_count.pl: Perl script for the computation of semantic relatedness
