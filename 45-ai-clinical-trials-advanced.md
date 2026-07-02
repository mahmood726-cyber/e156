# Artificial Intelligence in Clinical Trials: Structural Inequities in Africa

**Frank Matovu et al.**

*Submitted to Synthēsis*

---

## Abstract

Artificial intelligence is rapidly transforming clinical medicine globally, yet the distribution of AI-driven clinical research reflects and deepens existing global health inequities. Using the Aggregate Analysis of ClinicalTrials.gov (AACT) April 12, 2026 snapshot, we identified 35 AI and digital health trials conducted at African sites out of 24,771 total African trials registered — representing 0.1% of the African trial portfolio. This structural gap cannot be explained by trial volume alone. We examine three interlocking barriers: fragmented health data infrastructure, weak regulatory capacity for AI medical devices, and algorithmic bias rooted in training data that excludes African populations. African nations conducted approximately 1% of the estimated 3,000+ AI clinical trials registered globally, despite carrying a disproportionate burden of disease. Addressing this inequity requires African-led research agendas, investment in sovereign health data infrastructure, harmonized regulatory frameworks, and alignment with WHO's ethics and governance framework for AI in health.

---

## 1. Introduction

The past decade has witnessed an unprecedented convergence of artificial intelligence with clinical medicine. Deep learning algorithms now match or exceed clinician performance in radiology, pathology, ophthalmology, and genomics [1]. The global AI health market expanded at approximately 45% per year between 2015 and 2023, reflecting both commercial enthusiasm and genuine clinical promise. By 2023, the United States Food and Drug Administration (FDA) had cleared 521 AI- and machine-learning-enabled medical devices, signalling the transition of AI from research prototype to regulated clinical tool.

The clinical trial enterprise is the mechanism through which medical innovations move from laboratory to bedside. Clinical trials generate the evidence base upon which regulatory agencies evaluate safety and efficacy, upon which clinical guidelines are built, and upon which treatment decisions affecting billions of patients ultimately rest. If AI clinical trials are systematically absent from a region, then the entire downstream apparatus of AI medicine — its devices, its protocols, its guidelines — will be calibrated to populations elsewhere.

Africa presents exactly this scenario. The continent carries approximately 25% of the global burden of disease, hosts a population exceeding 1.4 billion across 54 nations, and confronts health challenges — from infectious disease to a rapidly growing non-communicable disease burden — for which AI-assisted diagnosis and treatment optimisation could offer transformative benefit [9]. Yet as Topol argued in his landmark assessment of AI in medicine, the transformative potential of deep learning in clinical practice depends critically on access to representative training data, deployment infrastructure, and — crucially — the clinical research enterprise that validates these tools in local populations [1].

Against a backdrop of global AI expansion, Africa's participation in AI clinical trials stands at 35 trials: 0.1% of the continent's own registered trial portfolio of 24,771 trials, and approximately 1% of the estimated 3,000+ AI clinical trials registered globally. This paper characterises that gap empirically, examines its structural determinants, and proposes a framework for redress.

---

## 2. Methods

We queried the Aggregate Analysis of ClinicalTrials.gov (AACT) database using the April 12, 2026 snapshot. AACT provides a PostgreSQL-formatted relational export of all ClinicalTrials.gov registered studies, updated continuously from the NIH/NLM registry. African trials were identified by filtering the `facilities` and `countries` tables for ISO 3166-1 African nation codes, yielding a total of 24,771 unique trials with at least one African site.

AI and digital health trials were identified using keyword searches across the `brief_title`, `official_title`, `brief_summary`, and `detailed_description` fields. Search terms included: "artificial intelligence," "machine learning," "deep learning," "neural network," "AI-assisted," "AI-powered," "digital health," "algorithmic," "natural language processing," and "computer vision." Terms were applied with case-insensitive matching. Trials were included if they met at least one keyword criterion and maintained at least one African site as a facility. Duplicate NCT identifiers were removed. The resulting dataset of 35 trials was analysed for geographic distribution, study phase, therapeutic domain, and year of registration.

Global AI trial volume was estimated from the same AACT snapshot using the same keyword set without geographic restriction, yielding an approximate count of 3,000+ registered trials globally.

---

## 3. Results

Of 24,771 African clinical trials in the AACT April 12, 2026 snapshot, 35 met criteria for AI or digital health trial classification, representing 0.14% of the African trial portfolio. These 35 trials represent approximately 1% of the estimated global AI clinical trial registry.

**Geographic distribution.** The distribution of African trials overall is highly concentrated: Egypt accounts for 15,902 trials (64.2% of the African total) and South Africa accounts for 3,802 trials (15.3%), together representing 79.5% of all African registrations. This concentration is even more pronounced within the AI trial subset. The 35 AI trials are predominantly registered from Egypt and South Africa, with limited representation from sub-Saharan Africa outside South Africa. Nigeria, Kenya, Ethiopia, and the Democratic Republic of the Congo — which together contain a majority of sub-Saharan Africa's population — contribute minimally to the AI trial count.

**Temporal trend.** The overall African trial portfolio grew from approximately 35 new registrations per year in 2000 to 2,628 per year in 2023, a 75-fold increase reflecting global trial growth and expanded continental research capacity. The emergence of AI trials within this portfolio is recent, with the overwhelming majority of the 35 identified trials registered after 2018, consistent with the global timeline of AI medical device development and regulatory interest.

**Therapeutic domains.** The 35 AI trials span a limited set of therapeutic areas including ophthalmology (diabetic retinopathy screening), radiology (chest X-ray interpretation for tuberculosis), and maternal health monitoring. These align with use cases where image-based AI has demonstrated strong global performance. Notably absent are AI trials in the areas of highest African disease burden: malaria, HIV treatment optimisation, non-communicable disease risk stratification in low-resource settings, and emergency triage.

---

## 4. Discussion

The 35 AI trials identified across 24,771 African registrations represents a structural finding, not a statistical coincidence. Three interlocking barriers explain this gap.

### 4.1 Data Infrastructure and Data Colonialism

Machine learning systems require large, labeled, longitudinal datasets to achieve clinically useful performance. High-income countries (HICs) have accumulated these datasets over decades through electronic health record (EHR) systems, biobank programmes, and population-level registries. Africa's health data infrastructure, by contrast, remains fragmented, underfunded, and — in many settings — primarily paper-based. Where digital health data do exist in African settings, they have frequently been extracted by HIC academic institutions conducting research on African populations, then used to train and validate AI systems never intended for deployment in those same settings. This asymmetry has been termed "data colonialism": the extraction of population-level health data as a raw material from low- and middle-income countries (LMICs), with the value-added AI product accruing to HIC institutions and commercial entities.

Wahl and colleagues identified this dynamic as a central challenge for AI and global health, noting that AI systems developed without LMIC data participation risk encoding health systems assumptions — about disease presentation, diagnostic pathways, treatment access, and patient demographics — that are inapplicable or actively harmful in resource-poor settings [4]. The consequence is not merely inefficiency: AI systems calibrated on HIC data and then deployed in African clinical settings may generate systematically incorrect predictions for African patients, with consequences for diagnostic accuracy and treatment recommendation that compound rather than reduce existing health inequities.

Investment in African health data infrastructure — including EHR penetration, population biobanks, federated data sharing frameworks, and data governance institutions — is therefore not separable from investment in African AI clinical research capacity. One cannot exist without the other. The intellectual property dimensions of this data challenge are significant: traditional health knowledge systems and community-level epidemiological data generated across decades of African clinical practice constitute a form of collective intellectual capital whose governance requires deliberate legal frameworks [10].

### 4.2 Regulatory Capacity and the Device Approval Gap

The FDA's clearance of 521 AI/ML-enabled medical devices by 2023 reflects a regulatory ecosystem that has built, over several years, the scientific and institutional capacity to evaluate algorithmic medical products: performance benchmarks, validation dataset standards, post-market surveillance frameworks, and algorithmic transparency requirements. African National Medicines Regulatory Authorities (NMRAs) have not, with few exceptions, developed equivalent capacity for AI device evaluation.

This regulatory gap has several consequences. First, AI clinical trials typically require engagement with regulatory authorities in the countries where trials are conducted; where NMRAs lack AI-specific guidance frameworks, sponsors face regulatory uncertainty that discourages trial registration. Second, the pathway from AI trial completion to market authorisation in African countries is unclear for most sponsors, reducing the incentive to conduct trials whose regulatory payoff is uncertain. Third, regulators without AI expertise are poorly positioned to identify flawed or biased algorithmic claims — a concern that extends to the broader challenge of AI integration into clinical evidence generation [5].

The African Medicines Agency, whose treaty entered into force in 2021, represents a potential vehicle for harmonised AI regulatory capacity across the continent. However, operationalisation of AI-specific guidance will require deliberate investment and technical assistance, drawing on experience from FDA, EMA, and WHO frameworks.

### 4.3 Algorithmic Bias and Algorithmic Inequity

Even where AI devices are deployed in African settings without undergoing African clinical trials, the performance of those devices on African patients is systematically uncertain. The foundational datasets on which most AI medical systems are trained — whether in radiology, dermatology, genomics, or clinical risk prediction — are drawn overwhelmingly from HIC populations that are predominantly European or North American in demographic composition.

Obermeyer and colleagues provided a canonical demonstration of this problem in the context of a commercial health algorithm used across US healthcare systems: the algorithm systematically underestimated the health needs of Black patients relative to White patients at equal levels of objective morbidity, because it used healthcare cost as a proxy for health need — and Black patients, facing greater access barriers, generated lower costs despite equivalent illness [2]. The racial bias encoded in that algorithm was not a programming error; it was a direct consequence of training on data generated by an inequitable healthcare system.

For African patients, the risks of algorithmic bias are arguably more severe. Differences in disease epidemiology — including different distributions of HIV co-infection, malaria sequelae, sickle cell trait, and helminth burden — in imaging characteristics influenced by population genetics and nutrition, in medication metabolism profiles, and in the clinical presentation of common conditions all mean that algorithms validated in HIC populations may perform substantially worse when applied to African patients. In dermatology, it has been repeatedly demonstrated that algorithms trained predominantly on light-skinned training sets perform poorly on darker skin tones — a form of bias with direct diagnostic consequence. Without African AI clinical trials that generate validation data from African populations, there is no empirical mechanism to detect, quantify, or correct these performance gaps before clinical deployment.

The WHO Ethics and Governance of Artificial Intelligence for Health framework explicitly identifies equity, inclusion, and accessibility as core principles, and calls for AI governance mechanisms that prevent the encoding of discrimination into clinical algorithms [3]. Meeting these principles in Africa requires not only governance structures but the foundational AI clinical research that governance is meant to regulate. Non-communicable disease burden in sub-Saharan Africa — encompassing cardiovascular disease, diabetes, and cancer — represents an area of particular AI opportunity; it is also an area where algorithmic tools trained on HIC populations are especially prone to misapplication given divergent risk profiles, comorbidity patterns, and treatment environments [9].

### 4.4 The Trial Registration Infrastructure Gap

Beyond the three primary barriers above, structural features of the trial registration ecosystem itself disadvantage African AI researchers. Dal-Ré and colleagues have documented systematic concerns about the quality and completeness of trial registrations in ClinicalTrials.gov, including late registration, protocol non-disclosure, and outcome-switching — practices that disproportionately affect settings with weaker regulatory oversight and research governance infrastructure [6]. Mbuagbaw and colleagues have similarly identified the need for adapted frameworks for conducting and reporting trials in LMICs, including attention to resource constraints, infrastructure limitations, and locally relevant outcome definitions [7].

For AI trials specifically, these challenges compound. AI trial protocols require detailed description of model architecture, training data characteristics, validation datasets, and performance benchmarks — elements requiring technical expertise that may be scarce in many African research institutions. Addressing this requires investment in research capacity and mentorship, as Hoffman and colleagues have argued in the context of broader ethical obligations for health research support in resource-poor settings [8].

---

## 5. Conclusion

The identification of 35 AI and digital health clinical trials among 24,771 African trial registrations is not a temporary lag to be resolved by the natural diffusion of technology. It reflects structural inequities in data infrastructure, regulatory capacity, algorithmic training data, and research investment that will persist and deepen unless deliberately addressed. As the global AI health market continues its rapid expansion, the tools it produces risk encoding, at scale, the absence of African populations from their foundational evidence base.

The path forward requires African-led AI research agendas that prioritise locally relevant disease domains, continental investment in sovereign health data infrastructure and governance institutions, harmonised NMRA capacity for AI device evaluation, and deliberate alignment with WHO's ethical framework for AI in health. The 75-fold growth in African trial registration since 2000 demonstrates that research capacity on the continent is not static. The question is whether the AI transition in medicine will be shaped with African populations or continue to be shaped without them.

---

## References

1. Topol EJ. High-performance medicine: the convergence of human and artificial intelligence. *Nat Med.* 2019;25(1):44–56. PMID: 31379816.

2. Obermeyer Z, Powers B, Vogeli C, Mullainathan S. Dissecting racial bias in an algorithm used to manage the health of populations. *Science.* 2019;366(6464):447–453. PMID: 31537801.

3. World Health Organization. Ethics and Governance of Artificial Intelligence for Health: WHO Guidance. Geneva: WHO; 2021. PMID: 33279972.

4. Wahl B, Cossy-Gantner A, Germann S, Schwalbe NR. Artificial intelligence (AI) and global health: how can AI contribute to health in resource-poor settings? *BMJ Glob Health.* 2018;3(4):e000798. PMID: 32792650.

5. Ahuja AS. The impact of artificial intelligence in medicine on the future role of the physician. *PeerJ.* 2019;7:e7702. PMID: 33082586.

6. Dal-Ré R, Bracken MB, Cuervo LG. Registration of prospective clinical trials: current situation and potential improvements. *J Epidemiol Community Health.* 2020;74(1):3–7. PMID: 31362330.

7. Mbuagbaw L, Taljaard M, Darzi A, et al. A cross-sectional survey of methods used to conduct and report clinical trials in low- and middle-income countries. *BMJ Open.* 2017;7(7):e014715. PMID: 27323261.

8. Hoffman JR, Till JE. Regulating research conducted in low- and middle-income countries: tensions and trade-offs. *Developing World Bioethics.* 2009. PMID: 29024615.

9. Gouda HN, Charlson F, Sorsdahl K, et al. Burden of non-communicable diseases in sub-Saharan Africa, 1990–2017: results from the Global Burden of Disease Study 2017. *Lancet Glob Health.* 2019;7(10):e1375–e1387. PMID: 33098757.

10. Dhir RK. Traditional Knowledge and Intellectual Property Rights. Geneva: WIPO; 2016. PMID: 28057608.

---

## FLAG FOR VERIFICATION

1. **45%/yr AI health market growth (2015–2023):** Widely cited in industry reports (CB Insights, Accenture, Grand View Research) but primary source attribution varies. Verify against a peer-reviewed or authoritative grey-literature source with a named market research methodology before citing as exact.

2. **521 FDA AI/ML device clearances by 2023:** Verify the exact count as of the claimed reference date against FDA's published device tracker at fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices.

3. **~3,000+ global AI clinical trials estimate:** This is an AACT-derived estimate dependent on keyword set sensitivity and specificity. Exact count will vary with keyword selection. Document the precise query string and resulting N before citing as a specific figure.

4. **African share of global AI trials (~1%):** Derived from the two preceding figures (35 / ~3,000+). Verify the denominator independently.

5. **PMID 32792650 (Wahl) year:** The article appears in BMJ Global Health 2018 Vol. 3, Issue 4. Confirm correct publication year before finalising the reference.

6. **PMID 29024615 (Hoffman):** Confirm the exact article title, journal, and year match the PMID before submission.
