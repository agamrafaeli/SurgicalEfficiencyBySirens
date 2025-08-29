# Methodology

Primary estimands: causal effect of acute siren exposure during or immediately before surgery on probability of each complication type: intraoperative, short-term postoperative, and (when available) long-term complications.

There is no single “successful/unsuccessful” outcome in the pipeline. Instead, analyses target each complication indicator separately. In the Israeli datasets currently available, long-term complications are generally not yet observable; the column `complication_long_term` is therefore optional and analyses typically focus on `complication_intraop` and `complication_short_term`.

A principled approach to aggregating these outcomes (e.g., weighted composite, multi-state modeling, utility-based scoring) is to be developed in future work and is explicitly out of scope for the current codebase.

We treat siren occurrence as a natural experiment and adjust for case mix using covariates such as urgency, wound class, ASA class, time of day, and staffing metrics. Models include logistic regression, generalized estimating equations, difference-in-differences, Cox proportional hazards, and propensity weighting.

Limitations include measurement error in event timings, potential residual confounding, and changes in case scheduling during conflicts. All outputs use de-identified hashes only.
