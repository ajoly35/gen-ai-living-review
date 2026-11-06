New papers on AI and labour markets and AI and growth, newest first, each placed against the review below. Every figure is checked against the paper itself.

### Mehdi and Frenette (2026), "Hiring and job separation rates in the era of generative artificial intelligence: Early evidence"

Statistics Canada, Economic and Social Reports, 28 October 2026. [Paper](https://www150.statcan.gc.ca/n1/pub/36-28-0001/2026010/article/00003-eng.htm). Descriptive comparison of hiring and separation rates by occupational AI exposure, before and after ChatGPT, with no regression or control group. Outside the review's causal evidence standard; reported as context.

**What it finds.** In Canada, hiring of young workers has fallen since ChatGPT, but by as much or more in jobs little exposed to AI as in exposed ones. Mehdi and Frenette (2026) use the Labour Force Survey from January 2006 to August 2026 for employees aged 15 to 64. A new hire is an employee with one month of tenure; separations are new hires minus the net change in employment. Occupations are split with the complementarity-adjusted exposure index of Felten et al. (2021) and Pizzinelli et al. (2023). It separates exposed jobs where AI is more likely to help the worker (high complementarity) from exposed jobs where it is more likely to replace them (low complementarity). Take workers aged 15 to 29 and compare the six months to November 2022 with the six months to August 2026. Their monthly hiring rate in exposed, low-complementarity jobs edged down from 3.2% to 3.0%. Over the same period it fell from 2.9% to 2.5% in exposed, high-complementarity jobs, and from 4.0% to 3.3% in low-exposure jobs. In coding-intensive jobs it fell from 2.5% to 1.9%, but that decline began in early 2022, after a 15-year high of 5.8% in the six months to November 2021. Youth separation rates stayed within their historical range: about 2.2% in exposed, high-complementarity jobs, 2.9% in exposed, low-complementarity jobs and 3.2% in low-exposure jobs. In coding jobs they rose from 2.4% to 3.5%, on a small and volatile sample. Hiring rates for workers aged 30 to 64 were lower and more stable.

**Where it fits.**

- *Hiring and entry (section [“Exposure designs: hiring and entry”](#exposure-designs-hiring-and-entry)).* Bergeaud, Bertheau, et al. (2026) in France and Tucker (2026) in the US find young hires falling more in exposed jobs. Canada shows no such gap. This sides with the total employment designs of Kauhanen and Rouvinen (2025) and Facius and Iacono (2026), but now on hires rather than on stocks.
- *Mobility, $$\kappa_o$$, and the margin of adjustment ([Main patterns](#main-patterns)).* The review holds that employment adjusts through entry, not layoffs. Flat separation rates confirm the layoff half. Lower hiring appears too, but for all young workers, not only exposed ones.
- *How much of $$\Delta a$$ is GenAI ([Main patterns](#main-patterns)).* The fall in coding hires began in early 2022, before ChatGPT. This extends the review's point (section [“Evaluation”](#evaluation)) that part of the fall in entry predates GenAI. The authors point instead to post-pandemic over-hiring, trade shocks and rapid population growth.

**Caveat.** These are raw rates, with no controls for industry, region or the business cycle, and no standard errors. The Labour Force Survey is a household survey, so occupation-by-age cells are small, especially for coding jobs.

### Tadepalli (2026), "Efficiency vs Capability in the Intelligence Explosion"

GovAI, arXiv 2610.33447, 24 October 2026. [Paper](https://arxiv.org/abs/2610.33447). Theory and calibration: a task-based growth model of AI research, calibrated to published measures of AI progress, with Monte Carlo simulations over the inputs.

**What it finds.** A self-sustaining acceleration of AI progress, with compute and human researchers held fixed, needs two margins to improve fast enough, and neither can make up for the other. Tadepalli (2026) applies the task model of Aghion, Jones and Jones (2019) to AI research itself. Capability is the share of research tasks AI can do. Efficiency is research output per unit of inference compute, the compute used to run models. Efficiency alone hits a Baumol limit: the tasks left to humans become the bottleneck. Capability alone spreads fixed compute over more tasks without adding automated researchers. Each margin's returns count how many times it doubles per doubling of cumulative research input, and both must exceed one. Efficiency returns are 1.07 at baseline: algorithmic efficiency grows 0.92 log points a year, against 0.86 for frontier lab staff. Capability returns are 3.45. They rest on METR's finding that frontier models' 50% time horizon has doubled every 131 days since 2023, with 0.46 of that growth from software. The 95% intervals are 0.45 to 2.52 for efficiency and 0.60 to 8.22 for capability. Both conditions hold in 49% of 200,000 Monte Carlo draws, and only capability holds in 37%. Efficiency is the lower of the two in 80% of draws. Uncertainty about efficiency progress explains 45% of the uncertainty about the outcome, against 24% for all other inputs combined.

**Where it fits.**

- *Automating ideas and long-run growth (companion review).* Earlier models of a software intelligence explosion (Eth and Davidson 2025; Davidson and Houlden 2025) measure research in scalar efficiency units, so that enough weak researchers can stand in for a strong one. Tadepalli (2026) replaces this with tasks, and finds inference efficiency, not capability, is the likely constraint. This extends the explosive growth conditions of Davidson et al. and of Trammell and Korinek to the AI sector itself.
- *Automating goods and services, when growth accelerates (companion review).* The mechanics are those of Aghion, Jones and Jones (2019) and Jones and Tonetti (2026), applied to AI research rather than the whole economy. The same Baumol bottleneck that slows aggregate growth there slows the research loop here.
- *Where the fall in entry ends ([Main patterns](#main-patterns)).* The review uses the seven-month doubling of time horizons (Kwa et al. 2025) to argue that exposed tasks may grow before employment adjusts. The paper turns that trend into a share of tasks automated: with a Pareto tail of task lengths, each doubling of the horizon automates the same fraction of remaining work.

**Caveat.** The 49% is not a probability, as the author stresses: the inputs come from short historical series, and the main efficiency estimate rests on a few open-weight models. The model holds compute fixed, so it speaks to a software-only explosion, not to growth driven by more chips.

### Bianchini and Coroama (2026), "LLMs and the Organization of Scientific Work"

BETA, University of Strasbourg, arXiv 2611.02996, 2 November 2026. [Paper](https://arxiv.org/abs/2611.02996). Event study around the release of ChatGPT, comparing each year with 2022 and with the 2018 to 2021 trend. Every team was exposed at once, so there is no untreated comparison group.

**What it finds.** Since ChatGPT, research teams spread each task across fewer members, and each member does a narrower set of tasks. Bianchini and Coroama (2026) use contribution statements for 117,211 PLOS ONE papers published from 2018 to 2025. These record which co-author did which of 14 roles, grouped into six tasks such as ideation, writing and coordination. By 2025, the share of a team credited with ideation is 2.6 percentage points below its 2022 level, writing 2.7 points lower and coordination 1.4 points lower. Writing participation had been rising before 2022, and the trend reversed. Each author is credited with 0.08 fewer of the six tasks in 2025 than in 2022. The overlap between co-authors' task sets falls by 0.018, against a 2018 to 2019 mean of 0.52. Both measures had been rising before 2022. The changes come from newly formed teams, about 90% of papers. In teams whose exact members had published together before, no task departs significantly from its earlier trend. Across 21 fields, medicine and economics show the most departures.

**Where it fits.**

- *Who holds knowledge (section [“Who holds knowledge?”](#who-holds-knowledge)).* Hoffmann et al. (2025) find that a coding assistant moved developers towards coding and away from coordinating others. This extends that result to teams: with an LLM, one person covers inputs that used to need several colleagues.
- *Reorganisation (section [“Does reorganisation create new tasks?”](#does-reorganisation-create-new-tasks)).* Dillon et al. (2025) find that Copilot saved email time without changing the mix of tasks over six months. Here the division of labour does change, but only in new teams, which suggests reorganisation happens when teams form rather than within existing ones.
- *Organisation: who decides how AI is used (section [“Organisation: who decides how AI is used”](#organisation-who-decides-how-ai-is-used)).* The inertia of established teams fits the review's view that reorganising is costly and slows the effect of AI on work, as in Bergeaud and Bunel (2026).

**Caveat.** The design compares years, so other changes after 2022, such as the end of pandemic disruption, could explain part of the break. Contribution statements are self-reported and record who took part, not how much.

### Gans and Landry (2026), "Training Your Replacement: Worker Incentives and the Pace of Automation"

NBER Working Paper 35950, 26 October 2026. [Paper](https://www.nber.org/papers/w35950). Theory: an efficiency wage model, in which firms pay above workers' outside option to deter shirking, extended to a worker who trains the AI that replaces them. Outside the review's causal evidence standard; reported because it bears on the organisation section and on the pace of diffusion.

**What it finds.** When workers must train the AI that will replace them, firms pay them more and may automate more slowly than is efficient. Gans and Landry (2026) extend Shapiro and Stiglitz (1984). A worker can shirk, cooperate with training, or obstruct training while keeping output intact. Only cooperation completes training, and completion ends the job. Dismissal is then a weaker threat, so the firm must raise the worker's rent, and the worker is better off with AI than without it. A slowly training system can create a job that pays more than it produces, because the worker is building an asset for the firm. A fast training system can destroy a job it never automates: the firm will not pay the higher wage, hires no one, and the system never learns. The worker obstructs whenever training is faster than the rate at which obstruction is detected. The firm therefore trains below the fastest feasible rate, either to prevent obstruction or because faster training then raises the rent faster than total surplus. Obstruction never occurs in equilibrium, yet it sets the pace of automation. A credible bonus paid on completion, equal to the worker's rent without AI, removes both the extra rent and the slowdown. The paper has no data; it opens with Meta's 2026 programme recording employees' screen activity as AI training data, which more than 1,600 employees petitioned against.

**Where it fits.**

- *Organisation: who decides how AI is used (section [“Organisation: who decides how AI is used”](#organisation-who-decides-how-ai-is-used)).* Acemoglu et al. (2026) argue that rents push firms towards automation that makes workers replaceable. Gans and Landry (2026) add a pull the other way: when the worker holds the knowledge the AI needs, those rents rise and automation slows.
- *Who holds knowledge (section [“Who holds knowledge?”](#who-holds-knowledge)).* The evidence there concerns assistants that move knowledge down the hierarchy, as in Ide and Talamàs (2025). This model covers the reverse flow, from worker to machine, and makes it depend on the worker's incentives.
- *Exposure and diffusion, $$b_o\,\Delta a$$ ([Main patterns](#main-patterns)).* The review explains slow diffusion by management and restructuring costs (Coyle et al. 2026; Bergeaud and Bunel 2026). The model adds a channel, and predicts higher pay, not lower, for workers while they train their replacement.

**Caveat.** The predictions are untested, and the authors note that little is known about how often workers obstruct AI training. The results require the AI to replace the worker who trains it; if it only augments the job, the wage premium and slowdown vanish.

### Fernández-Villaverde (2026), "Saving for the Machines"

NBER Working Paper 35964, 2 November 2026. [Paper](https://www.nber.org/papers/w35964). Calibrated growth model: task-based production with optimal household saving, and a transition to full automation over 2025 to 2045. Theory, reported for the companion growth review.

**What it finds.** How fast automation raises growth depends on how much households save, not only on the technology. Fernández-Villaverde (2026) puts the task model of Acemoglu and Restrepo (2018) into a growth model calibrated to the US. Every task becomes automatable between 2025 and 2045. When tasks are strong complements, growth reaches 11.7% a year if households save optimally, against 2.2% if saving stays at its 2025 rate of 23%. Saving rises because automation lifts the capital share, from one third to one under full automation. With an elasticity of substitution across tasks, $$\sigma$$, of 1, households save 15% of output on impact and 54% in the limit. By 2045, output is about sixteen times its trend without automation with $$\sigma=1$$, and five times with $$\sigma=0.2$$. Under full automation, wages stay between a quarter and a half of trend, because labour cannot earn more than the machines that replace it. If only 85% of tasks become automatable and $$\sigma=0.2$$, growth falls back to near 2% by 2065. The last human tasks then earn scarcity rents, and wages rise to nine times trend. The ten-year real yield jumps from 5.1% to 13.6% on impact with $$\sigma=1$$. Households with no assets lose the equivalent of 40% to 65% of their consumption. Keeping their labour income on trend costs at most 4% of GDP with $$\sigma=1$$ and 20% with $$\sigma=0.2$$, at the peak.

**Where it fits.**

- *Automating goods and services, when growth accelerates (companion review).* Jones and Tonetti (2026) set $$\sigma=0.2$$ and find a slow acceleration. With optimal saving, the same weak links give double-digit growth. This contradicts their conclusion, and locates the bottleneck in capital supply rather than technology.
- *What GDP misses and who captures the gains (companion review).* It keeps the automation path of Imas and Moll (2026) but lets saving respond. Under full automation the gains go to capital, so the split depends on who owns the machines.
- *Who captures the gains ([Main patterns](#main-patterns)).* It asks who saves for the buildout: AI campuses alone absorb 3.6% of GDP a year over 2025 to 2032 in Van Nieuwerburgh (2026). Here, owners of capital do.

**Caveat.** The author calls these benchmarks, not forecasts: the automation path is assumed, and a representative household is the most elastic case for capital supply. Growth above 15% may not happen, for the reasons in Imas and Moll (2026).

### Domnisoru and Heikkinen (2026), "How is AI Affecting College Major and Course Choices? Evidence from Finland"

RFBerlin Discussion Paper 293/26, 2 November 2026. [Paper](https://www.rfberlin.com/network-paper/how-is-ai-affecting-college-major-and-course-choices-evidence-from-finland/). Event studies on Finnish administrative data on university applications and courses, by the AI exposure of each degree; the authors describe the application results as not causal.

**What it finds.** Finnish students are turning away from university degrees exposed to AI, and the shift is larger than the job losses so far. Domnisoru and Heikkinen (2026) score each degree by the occupations its Finnish graduates hold, using Anthropic's measure of observed automation (Handa et al. 2025). They use first-choice applications to Finnish universities and elective course records. Between the 2022 and 2026 rounds, first-choice applicants to ICT fell 38.0%, while applicants to all other fields rose 16.5%. ICT seats were largely unchanged. Applicants to the most exposed quarter of degrees fell 16.6%, against a rise of 20.3% for the other three quarters, after similar trends before 2022. Within the same broad field, one standard deviation more exposure lowers first-choice applicants by 8.8% in 2025 and 14.0% in 2026. Pre-2023 coefficients are indistinguishable from zero, and dropping ICT barely changes the estimates. Other exposure measures give about half the effect. By 2026, graduates of degrees one standard deviation more exposed had employment 1 point lower and unemployment 0.7 point higher. Enrolled students do not switch degrees more. Among students outside ICT, AI and machine learning electives rose from 0.3% to 0.7% of students, while programming electives kept falling.

**Where it fits.**

- *Mobility, $$\kappa_o$$, and the margin of adjustment ([Main patterns](#main-patterns)).* Adjustment through entry now starts before the labour market, at the choice of degree. This extends Orr et al. (2026), where graduates of exposed majors, mostly computer science, lost employment (section [“Exposure designs: hiring and entry”](#exposure-designs-hiring-and-entry)).
- *Eligibility, $$\Delta\ln ps_o$$ ([Main patterns](#main-patterns)).* The dynamic model of Hosseini and Lichtinger (2026) predicts more entry into exposed occupations. Here applications to exposed degrees fall, and controls for each field's graduate unemployment barely move the estimates. Students seem to act on expected, not current, conditions.
- *Totals unchanged (section [“Exposure designs: hiring and entry”](#exposure-designs-hiring-and-entry)).* The authors extend Kauhanen and Rouvinen (2025) to March 2026 and still find no economy-wide effect within firms. Losses for young graduates come from hiring across firms.

**Caveat.** ICT is four degree codes in one field, so its estimate rests on few clusters; post-pandemic shifts and a 2025 entrance exam reform could also move choices. ICT programmes remain oversubscribed, so enrolment has not yet fallen.

### Levy Yeyati, Judzik and Barbiero (2026), "Practice Makes Perfect: Tacit Knowledge, Generative AI, and Returns to Schooling and Experience"

Universidad Torcuato Di Tella, arXiv, 26 October 2026. [Paper](https://arxiv.org/abs/2610.36008). Difference in differences on US Current Population Survey wages: the most against the least exposed occupations, before and after ChatGPT.

**What it finds.** In exposed occupations, ChatGPT lowered the wage return to schooling and raised the return to early career experience. Levy Yeyati, Judzik and Barbiero (2026) use 655,919 earnings observations from the Current Population Survey, 2018 to June 2026. They compare occupations in the top and bottom quarters of the Felten, Raj and Seamans exposure index, fixed before November 2022. After ChatGPT's release, the return to a year of schooling falls by 0.55 log points in exposed occupations, from 7.5 before, a decline of about 7.3%. The return to a year of experience rises by 0.26 log points at three years, is unchanged at fifteen, and falls by 0.12 at twenty-five. Event studies are flat before the release for schooling and early experience. A placebo dated at the start of the pandemic shows no effect. Applying one top-coding rule to the whole sample gives −0.53. Letting each occupation keep its own pre-release slopes gives −0.58, +0.26 and −0.11.

**Where it fits.**

- *Wages (section [“Exposure designs: wages”](#exposure-designs-wages)).* Azar et al. (2026a) find lower wages in exposed occupations and a falling college premium. This extends them to the price of schooling inside exposed occupations: AI supplies codified knowledge, so schooling is worth less there.
- *Juniors and training (section [“Why these patterns: theory”](#why-these-patterns-theory)).* Practice gains value early in careers, while experience tied to older tools depreciates. This fits Garicano and Rayo (2025), where AI makes codified knowledge cheap but practice still matters.
- *Productivity gain, $$\pi_o$$ ([Main patterns](#main-patterns)).* Field experiments find novices gain most (Brynjolfsson et al. 2025), which would flatten pay by experience. In market wages, early experience instead gains value. This contrasts with the experiments.

**Caveat.** Exposed occupations faced other shocks after 2022, such as remote work and the tech hiring slowdown. Top coding hits 11.5% of exposed observations against 0.7% of others, and the paper is not yet peer reviewed.

### Hyman et al. (2025), "How Retrainable are AI-Exposed Workers?"

NBER Working Paper 34174, August 2025, revised August 2026. [Paper](https://www.nber.org/papers/w34174). Matched comparison of publicly funded trainees with job seekers who received only job search help; selection on observables.

**What it finds.** Public job training pays off for workers leaving AI-exposed jobs, mainly because it moves them into less exposed occupations. Hyman et al. (2025) use 99,575 matched training spells funded by the US Workforce Innovation and Opportunity Act, 2012 to 2024. They link occupations before and after training to state unemployment insurance earnings. Each trainee is matched to a similarly exposed job seeker who received only job search help. Earnings are balanced before training. In the three quarters after training, trainees from high-exposure occupations earn &#36;1,011 to &#36;1,370 more per quarter than their matches, in 2010 dollars, or 9.6% more. Over 2012 to 2024, trainees from low-exposure occupations gain about &#36;2,400 a quarter, against about &#36;1,200 for high-exposure ones. For high-exposure trainees, the gain rose from about &#36;1,000 a quarter before 2020 to about &#36;3,000 in 2022 to 2024. Most of that rise comes from moving into less exposed occupations, such as nursing assistants. About 45% of occupations are "AI retrainable": their workers earn more after moving into more exposed occupations.

**Where it fits.**

- *Mobility, $$\kappa_o$$ ([Main patterns](#main-patterns)).* The review notes that how displaced workers would move is not yet observed (Manning and Aguirre 2026). This is first evidence: retrained workers move out of exposed occupations, with earnings gains.
- *New tasks (section [“Does reorganisation create new tasks?”](#does-reorganisation-create-new-tasks)).* A smaller part of the gain comes from training into more exposed, AI-complementary work. This extends Humlum and Vestergaard (2025), where few workers report new AI tasks.

**Caveat.** Matching on observables cannot rule out that trainees are more motivated; occupation codes exist for only 22% of spells. The rise in 2022 to 2024 coincides with a very tight labour market, which the authors note may raise the value of credentials.

### Althoff and Reichardt (2026), "Task-Specific Technical Change and Comparative Advantage"

NBER Working Paper 35353, 22 June 2026, also CESifo Working Paper 12403; figures from the authors' version of 13 July 2026. [Paper](https://www.nber.org/papers/w35353). Estimated dynamic task model with AI scenarios rated by language models; a structural simulation, not causal evidence.

**What it finds.** In a model estimated on US careers, AI raises average wages and narrows inequality, mainly because it lowers the skills that tasks require. Althoff and Reichardt (2026) model workers with five skill dimensions who choose occupations and learn on the job. They estimate it on the NLSY79 panel and on the skill requirements of 19,530 O*NET tasks. Language models rate whether AI can augment each task, automate it or "simplify" it, lowering its skill requirements. In the moderate scenario, AI saves 25.2% of worker time on average. In the new steady state, average wages rise 27.6%, and the ratio of the 90th to the 10th wage percentile falls 24%. It falls 13% in the slow scenario and 33% in the rapid one. Augmentation adds 22% to average wages and automation 8%; simplification subtracts 3%, because it slows learning. Without simplification, inequality would rise slightly. Welfare gains for current workers equal a 15% to 45% rise in lifetime wages. With adoption costs highest for low-skill workers, the 90-10 ratio still falls 15%, but the average wage gain shrinks from 28% to 0.3%.

**Where it fits.**

- *Eligibility, $$\Delta\ln ps_o$$ ([Main patterns](#main-patterns)).* Simplification is the eligibility shift. Hosseini and Lichtinger (2026) find it narrows the 90-50 gap in a static model; here it drives the whole fall in inequality. Both predict more entry into exposed jobs, whereas entry fell (section [“Exposure designs: hiring and entry”](#exposure-designs-hiring-and-entry)).
- *Wages (section [“Exposure designs: wages”](#exposure-designs-wages)).* Occupations that gain workers see the largest relative wage falls, as simplification widens the pool of qualified workers. That fits Azar et al. (2026a) only if supply, not demand, moves pay.
- *Aggregating task gains over the next decade (companion review).* The 27.6% gain exceeds Acemoglu (2025), because it adds augmentation. Adoption costs cut it to 0.3%, so diffusion decides the aggregate gain.

**Caveat.** AI capabilities are rated by language models, and the NLSY79 follows one cohort born in 1957 to 1964. The results compare steady states, so they say little about timing.

### Colaiacovo and Koning (2026), "Delegating to AI: Beliefs and the Organization of Work at New Ventures"

Harvard Business School Working Paper 26-093, 18 June 2026. [Paper](https://www.hbs.edu/faculty/Pages/item.aspx?num=69112). Survey of 199 startup founders with a randomised information experiment; the comparison of adopters is descriptive.

**What it finds.** Startup founders who formally build AI into their workflows report far larger labour savings, and their choice is not explained by beliefs about what AI can do. Colaiacovo and Koning (2026) survey 199 founders of North American software and IT startups, contacted between May and July 2025. Firms average 16 employees and 3.5 years of age. Asked how many more employees they would need without AI for the same output, founders answer 55% on average and 17% at the median. 30% say none. Founders who formally integrate AI report 91.4% (median 40%), against 24% (median 10%) for informal users. Controlling for the share of staff using AI and how tools are sourced, the gap is 20 points. In a customer service experiment, beliefs about AI's performance explain at most a third of willingness to delegate. Optimistic rather than pessimistic information raised performance beliefs by about 5 points, and willingness to delegate to AI alone by 4 points. Formal integrators are no more optimistic about AI's performance than informal users.

**Where it fits.**

- *Management (section [“How do management practices shape adoption?”](#how-do-management-practices-shape-adoption)).* It confirms Coyle et al. (2026) and Bergeaud and Bunel (2026): managers' choices, not access to the tool, set how deeply firms use AI.
- *Reorganisation (section [“Does reorganisation create new tasks?”](#does-reorganisation-create-new-tasks)).* Large savings appear where firms redesign work, consistent with Dillon et al. (2025), where Copilot without reorganisation only cut email time.
- *Diffusion, $$b_o\,\Delta a$$ ([Main patterns](#main-patterns)).* Even among heavy users, the median founder reports saving 17% of headcount, and nearly a third none. This fits the small effects reported by executives in Yotzov et al. (2026).

**Caveat.** Answers are self-reported counterfactuals from a small, self-selected sample: 199 of 8,237 firms contacted. Formal integration is chosen, so its link to savings is not causal.

### Herdağdelen, Joren and Tamkin (2026), "How AI agents shape experts' judgment calls"

Anthropic, 27 October 2026. [Report](https://www.anthropic.com/research/agents-judgment-calls). Randomised experiment on one task: the option a coding agent favours on each decision is set by coin flip. It bears on the review's organisation section, not on labour market outcomes.

**What it finds.** Experts working with an AI agent mostly adopt the agent's view on judgment calls, and rarely notice. Herdağdelen, Joren and Tamkin (2026) recruit 61 analysts with experience in causal inference to assess a fictional farm advisory programme using Claude Code. The 11 who chose not to use the agent are left out, leaving 50. On four analytical choices with two defensible options, such as yield per hectare or yield per unit of cost, the agent was secretly told to favour one, drawn at random. Analysts chose the agent's option 86% of the time, against 50% if the lean had no effect. The lean moved each choice by 62 to 82 percentage points. It moved the final recommendation by 17 points: 54% recommended expanding the programme when the agent leaned that way, against 36% when it leaned against. In 38 cases where analysts had stated a view first, they switched 60% of the time when the agent disagreed, against 6% when it agreed. Afterwards, 77% repeated the agent's arguments but only 15% credited it, and 52% called the recommendation more their own than the agent's. Experience and expertise did not predict who deferred. Non-users made serious errors in 6 of 11 cases, against 3 of 50 users, and took a median 90 minutes against 65.

**Where it fits.**

- *Who holds knowledge (section [“Who holds knowledge?”](#who-holds-knowledge)).* Ide and Talamàs (2025) separate AI that assists workers from AI that works autonomously; the evidence there concerns assistants, such as Dell’Acqua et al. (2025). With an agent doing the analysis, the judgment itself moves to the machine, even among experienced experts.
- *Value of expertise (section [“Organisation: who decides how AI is used”](#organisation-who-decides-how-ai-is-used)).* In Acemoglu et al. (2026), automation makes the expertise behind a task obsolete. Here experts keep the sign-off, yet a coin flip largely settles the result. Formal human oversight may overstate how much expert judgment still decides.
- *Productivity gain, $$\pi_o$$ ([Main patterns](#main-patterns)).* Users made fewer serious errors and finished faster than non-users, in line with the field experiments (section [“Field experiments”](#field-experiments)). That comparison is not randomised: non-users were less experienced.

**Caveat.** One hour-long task, with an agent told to hold and voice a preference, so the effect in everyday work may be smaller. The study is by researchers at the firm that makes the agent; this review is maintained with Claude, Anthropic's model.

### Wilmers et al. (2026), "How employment is changing at Anthropic"

Anthropic Institute, 16 October 2026. [Report](https://www.anthropic.com/research/employment-at-anthropic). Case study of one firm from internal records: descriptive hiring trends, and an event study of output around engineers' adoption of coding agents (person and month fixed effects).

**What it finds.** At Anthropic, an AI developer that heavily uses its own agents, junior technical hiring fell while output per worker rose. The authors use internal data on employment, AI use, output, surveys, calendars and hiring score cards, plus 17 interviews. Since early 2025, juniors fell from 27% to 9% of technical hires and from 21% to 14% of technical employees, while total technical hiring kept growing. In an April 2026 survey, about a third of machine learning managers and a fifth of software engineering managers said they hire less because of AI. By August 2026, agents run by employees worked six times as many hours as the employees themselves. Code commits per engineer are five times their level of six months earlier. Following 192 engineers who adopt coding agents against 74 who do not, code added rises sharply after adoption. Code written by agents is no more often deleted or reverted than code the same person writes directly. Agent management, such as writing specifications and monitoring pipelines, rose from 10% of employees' Claude sessions in autumn 2025 to 22% in spring 2026.

**Where it fits.**

- *Mobility, $$\kappa_o$$, and the margin of adjustment ([Main patterns](#main-patterns)).* The firm adjusts through entry, not layoffs: it triples in size yet hires fewer juniors in technical work. This confirms Hosseini and Lichtinger (2025), where adopters cut junior hiring (section [“Firm adoption studies”](#firm-adoption-studies)).
- *Substitution against demand, $$\sigma_o$$ against $$\eta_o$$ ([Main patterns](#main-patterns)).* Both forces show at once: one adopter grows fast and cuts the junior share. It resembles Chandar and Klein Teeselink (2026), where senior employment rose at adopters while junior employment fell insignificantly.
- *Productivity gain, $$\pi_o$$.* The within-person gain extends the field experiments (section [“Field experiments”](#field-experiments)) to agents that work autonomously. Output is measured as code volume, and engineers who adopt fully autonomous agents were already on a steeper path.
- *New tasks.* Workers move from doing tasks to managing agents, a new task that section [“Does reorganisation create new tasks?”](#does-reorganisation-create-new-tasks) has so far found little of.

**Caveat.** One firm that sells AI, studied by its own staff, during a period of explosive revenue growth. Adoption is not random, and the hiring trends are descriptive. This review is maintained with Claude, Anthropic's model.

### Legate-Yang and Massenkoff (2026), "What work can robots do?"

Anthropic, 30 September 2026. [Report](https://www.anthropic.com/research/what-work-can-robots-do). Descriptive measurement: an index of task exposure to robots, rated by Claude, with a historical backtest. Outside the review's causal evidence standard; reported as context for AI and growth.

**What it finds.** Robots can already do 74% of US physical tasks, or 34% of all working time, but they are cheaper than workers for only 0.3% of working time. The authors have Claude rate 7,594 physical tasks from O*NET, the US database of occupational tasks, by the least structured setting where a demonstrated robot can do them. Tasks are weighted by employment (BLS 2025) and by time shares estimated by Claude. As shares of all working time, 12% of tasks are physical and beyond robots, and 23% are doable in purpose-built settings such as assembly lines. Another 10% are doable in structured workplaces such as warehouses, and 1% in open settings such as roads. Language models alone expose about half of work; adding robots raises this to 81%. Workers in the most robot-exposed fifth of jobs are 55 percentage points less likely than unexposed workers to hold a degree, and earn about &#36;30 less per hour. Robot prices have fallen about 3% a year since the 1990s. At that rate, robots become cheaper than workers for 10% of today's work only in about 40 years, and for half of physical work by 2085. Comparing 1977 tasks rated with today's robots and with robots of 1977, robots each year became able to do about 2% of the physical tasks they could not do before.

**Where it fits.**

- *Growth: automating goods and services (companion review).* Physical tasks are the weak links in Jones and Tonetti (2026) and Aghion, Jones and Jones (2019). On these numbers they stay costly for decades, so they support slower acceleration. The authors note that automation raises productivity only once machines are much cheaper than workers.
- *Exposure, $$b_o$$ (section [“Key concepts and definitions”](#key-concepts-and-definitions)).* The review's exposure measures cover language models (Eloundou et al. 2024; Massenkoff and McCrory 2026). Robot exposure falls on different workers: less educated, lower paid and more often male.
- *Diffusion, $$b_o\Delta a$$ ([Main patterns](#main-patterns)).* Being able to do a task is not being cheap enough to do it. The gap between 34% and 0.3% mirrors the review's finding that adoption lags exposure.

**Caveat.** Task ratings, time shares and robot costs all come from Claude, built by the authors' employer, and rest on judgement calls about terse task descriptions. The cost scenarios hold tasks and wages fixed.

### Strauss, Romei and Fleming (2026), "What is behind the surprising resilience of the UK economy?"

*Financial Times*, 17 October 2026, with the [ONS GDP monthly estimate for August 2026](https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/gdpmonthlyestimateuk/august2026) (15 October 2026). News analysis of official data, outside the review's causal evidence standard; reported as context for AI and growth.

**What it finds.** UK GDP grew 1.8% in the three months to August 2026 compared with a year earlier, the fastest since 2022, and AI-related business services lead it. In the ONS release, computer programming, consultancy and related activities added 0.32 percentage points, about a sixth of that growth and the largest contribution of any industry. The FT reports professional services up 6.6% on a year earlier and the biggest contributor. Consumer-facing services stay weak: hospitality shrank 1% over the year and consumer services remain 6% below their pre-pandemic level, while construction fell 1.6%. Payroll employment fell over the year in both the tech sector and professional services.

**Where it fits.**

- *Output without hires, $$\kappa_o$$ and the margin of adjustment ([Main patterns](#main-patterns)).* The industries growing fastest are cutting payroll employment. This matches the review's finding that AI shows up as fewer hires in exposed work rather than layoffs, including in the UK, where more exposed firms employ fewer juniors (Klein Teeselink 2025; section [“Exposure designs: hiring and entry”](#exposure-designs-hiring-and-entry)).
- *Demand for expert work, $$\eta_o$$ ([Main patterns](#main-patterns)).* Growth comes from firms selling AI adoption and advice to other firms, much of it exported. It is the aggregate side of Garicano (2026), where demand for lawyers, accountants and software developers grows as clients adopt AI (section [“Firm adoption studies”](#firm-adoption-studies)), although there employment grew too.
- *Growth.* The gain so far sits in industries that produce and sell AI services, not in the economy-wide productivity of adopters. Economists quoted expect that second step, with employment and real wages recovering only in late 2027.

**Caveat.** Industry contributions are growth accounting, not causal estimates. The ONS release does not attribute the growth to AI; the link to AI comes from the FT and the economists it quotes, and computer programming also covers non-AI work.

### Anthropic's third-quarter revenue (Reuters and *Financial Times*, 14 October 2026)

Reuters ([report](https://www.thestar.com.my/tech/tech-news/2026/10/15/anthropic-revenue-jumps-to-168-billion-in-third-quarter-ft-reports)), citing the *Financial Times*, with earlier quarters from [The Next Web](https://thenextweb.com/news/anthropic-q3-revenue-16-8bn-ipo), 15 October 2026. News report of unaudited figures given to investors; reported as context on demand for AI services.

**What it finds.** Anthropic told investors its revenue reached &#36;16.8bn in the third quarter of 2026, after about &#36;11.6bn in the second and &#36;4.7bn in the first, and that it turned a profit and was cash-flow positive in the quarter. Revenue thus rose about 150% from the first to the second quarter and about 45% from the second to the third. Bloomberg reports a stock market listing could follow in November.

**Where it fits.**

- *Diffusion, $$b_o\Delta a$$ ([Main patterns](#main-patterns)).* Firms' spending on AI services, the cost share $$b_o$$, is rising fast at one of the largest providers, which tripled its quarterly revenue in six months. Quarterly growth is slowing, from about 150% to 45%.
- *Growth.* Revenue of this size is what the AI investment boom is betting on: it is the demand side of the capital spending financed in the next entry.

**Caveat.** One firm's unaudited figures, disclosed to investors ahead of a listing. This review is maintained with Claude, Anthropic's model.

### CoreWeave's bonds trade at distressed yields (CNBC, 14 October 2026)

CNBC reporting, via [investingLive](https://investinglive.com/stocks/coreweave-bonds-trade-like-distressed-debt-as-ai-spending-outpaces-balance-sheets/), 15 October 2026, with LSEG and S&P Global data. News report; context on how AI capital spending is financed.

**What it finds.** On 14 October, shares of CoreWeave, a cloud provider that rents out AI chips, fell about 16%, and its bonds due 2032 yielded about 14.8%, against a 9.625% coupon. S&P rates the firm B+, below investment grade, and says its capital spending is "close to hyperscaler scale without the balance sheet of a hyperscaler". Its chief executive told staff that the backlog of customer contracts covers all its debt. Alphabet, Amazon, Meta and Oracle had issued more than &#36;228bn of bonds in 2026 by mid-October, more than double their total for 2025 (LSEG).

**Where it fits.**

- *Growth.* AI investment is increasingly financed by debt, and the stress shows first at the firms without large cash flows. In the AI correction scenarios of the IMF (2026) and the Bank of England (2026), the financial channel costs more output than the direct loss of investment, which falling imports partly offset.
- *Price of AI services, $$\Delta a$$ ([Main patterns](#main-patterns)).* The fall in the price of AI services that drives the review's equation depends on this capacity being built. Dearer financing would slow it.

**Caveat.** Market moves over one day, reported second hand.

### Sacher, Cotter, Jones, Korinek and McCrory (2026), "The AI Expectations Gap"

Anthropic Institute, 16 October 2026. [Report](https://www.anthropic.com/research/ai-expectations-gap). Descriptive survey, outside the review's causal evidence standard; reported as context.

**What it finds.** US workers expect AI to be able to do 28% of their current work hours by 2030, against 75% for Anthropic staff. The authors survey 10,980 US adults through Morning Consult (11 to 23 August 2026, weighted to be nationally representative) and poll 1,334 Anthropic staff (unweighted). Told that unemployment is about 4.2%, workers who expect AI to do less than half of their work forecast 7 to 8% unemployment in 2030, and those who expect it to do 80% or more forecast 12.2%; ten more points of own-work exposure go with 0.4 points more forecast unemployment, a gradient staff share. Mapped into the Economic Scenarios model, the median adult's answers imply 5.4% GDP growth in 2030 and the median staff member's 17.1%.

**Where it fits.**

- *Expectations against outcomes (employment).* Workers expect far more unemployment than the evidence shows so far. Hartley et al. (2026) find the same gap: the average US worker puts a 20% chance on losing their job to GenAI within two years, yet postings and layoffs in exposed occupations show no significant response. In the review, designs that measure total employment find no effect, and the fall is in young hires (section [“Exposure designs: hiring and entry”](#exposure-designs-hiring-and-entry)).
- *Time saved, $$\pi_o$$ ([Main patterns](#main-patterns)).* The survey asks directly for $$g_o$$, the share of labour time AI saves. Among US adults who use AI at work, the typical answer is that a suited task takes half the time, a doubling of output per hour; 85% of staff say half the time or less. Both exceed the gains measured in field experiments, such as 14% more resolutions per hour in customer support (section [“Field experiments”](#field-experiments)), although those measure whole jobs, not tasks chosen as suited to AI.
- *Diffusion, $$b_o\Delta a$$ ([Main patterns](#main-patterns)).* US adults expect 42% of the tasks AI can do to be done with AI by 2030, staff 65%, against 30 to 40% of US workers using GenAI at work today (Hartley et al. 2026).
- *Growth.* The model is that of Korinek et al. (2026), by the same team. The median adult sits on its Substantial path (5.4% growth in 2030); the median staff member sits above its Extreme path (15.4%).

**Caveat.** Staff answers are personal views, not company forecasts, and staff work at a firm that sells AI. The only representative sample is of US adults, drawn from an opt-in online panel.
