# Maximum Likelihood Formulation


$P(K|r) = \prod_{f} P(K_f|r)  $    ***We want to find the region $r$ that maximizes P(K).***

$P(K_f|r) = \sum_{g_m,g_p \epsilon G} P(g_p|k_p)P(g_m|k_m) \prod_{c}P(k_{c}|g_{phase}(g_{p}, g_{m})) $  Expression for likelihood of family k-mer distribution.

$P(g_i|k) = \frac{P(k|g_i)}{\sum_{g_i\epsilon G} P(k|g_i)}  $  

Convert to log probability.

$log(P(K|r)) =  \sum_{fams}  \left ( log \sum_{g_{m_f}}\sum_{g_{p_f}} \prod_{c_f} P(k_{c_f}|g_p,g_m) - log \sum_{g_{p_f}} P(k_{p_f}|g_{p_f}) -  log \sum_{g_{m_f}} P(k_{m_f}|g_{m_f}) \right )$

$G = \left \{ 0/0,0/1,1/0,1/1 \right \}  $  Set of possible phased genotypes for k-mer.

$K$ = Distribution of a k-mer 

$r$ = region 

$f$ = family 

$c$ = children 

$g$ = phased genotype of k-mer 

$G$ = set of possible phased genotypes 

$g_{phase}$ = Phasing dictionary from Kelley's algorithm 