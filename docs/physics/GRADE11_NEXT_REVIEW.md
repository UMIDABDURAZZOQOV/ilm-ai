# Keyingi: 11-sinf §16–20 — 2026-10-26

286/316,30qolgan.15asl sahifa58–72 tasvirlari/nativehashlari qayta o‘qildi. Bu source review tayyorgarligi, yangiJSON/runtimehaliyo‘q. Mustaqilekspertapproval emas.

PDF58,59,60: Original idealinductor phasor/reactance checked. Choose passive terminalvoltage uL=L*di/dt and i=Imcos(theta): uL=-omegaLImsin(theta)=Umcos(theta+pi/2); source58 derivative+sin/cosidentity sign inconsistent, source59 voltageLEADScurrent90 conclusion correct. SelfEmf=-Ldi/dt vs terminaluL opposite. XL=omegaL=2pnuL,Im=Um/XL onlyidealL/steadySINUSOID, noRloss; fieldenergyexchange not allheat.

PDF60,61,62,63: Original SERIES RLC phasor/norm checked. Choose currentreference i=Imcos(theta), then totalu=Umcos(theta+phi); source60 gives bothcos withnooffset despitegenerallynonzerophase. Z=sqrt(R²+(XL-XC)²),Imax=Um/Z,voltagephasornorm NOTsumofmagnitudes. Source62tanphi denominator printedUm but correctUR (reactdiff/R nextcorrect); finite grader tanPhi=(XL-XC)/R signed/unbounded not sine/cosrange. No generalcomplexsolver/trigatan.

PDF63,64,65: Original fixedseriesRLC resonance criteria/voltagemagnification checked. XL=XC,omegarez=1/sqrtLC, Zmin=R>0 and Ipeak=Um/R forfixedUm/R/L/C frequency-independentidealcomponents. Rlarge stillreactivecancellationexists but broadlessvisiblepeak, not mathematicallynoresonance. Voltageindividualcanexceedsupply whenQ=sqrt(L/C)/R>1, notforALLcircuits. Source65C50Hz.1H~101.4uF approximated100uF acceptable statedrounding; new rationalrounding explicit. Alllowvoltageconditionalno physicalovervoltagetask.

PDF66,67: Original digitalresonance lab uses UL/UC vs frequency. Source66initialUC<UL thenincreasefrequencyuntilUC=UL is wrong fixedLC sweepdirection: above resonanceXL>XC, increasingf movesaway. Correct digitaltable beginsbelowresonanceUC>UL,passesUL=UCthenUL>UC. Original conditional data mathematically checked forR100ohm,L1H,C=1/(4*3.14²*100²)F,UsourceRMS1V:50HzUC1.33/UL.33;100Hz6.28/6.28;150Hz.79/1.77, rounded. No real instrument readings/20Vmeter or mainsinstruction claim. Sampledequalitywithinmodel, threepointsnotallcontinuouscurveproof.

PDF67,68,69,70,71,72: Original sinusoidalRMSaveragepower/factor equations checked. Pavg=UeffIeffcosPhi, A=Pavg*t forsteadyintegercycles/wholeperiodaverage, passivefixedseriesRLCfactor0..1, R/Z notarbitraryactivegeneratorcosbound. Source67 usesu*i*t asworkonlysmallintervalapprox, notexactarbitrarytimephase; source68halfperiodpositive/halfnegative notuniversally foranyphi, onlyspecialreactivecase. Source70=.85cos policy not asserted universalcurrentlegalrequirement; noDIYcompensation. Source70sample cos~.5427 and P~132.5W correct reference but printedcos²/fractionderivation inconsistent notcopied. Source71q4LC1H/2.5uFomega~632rad/s not630e6;source71q6firstequalenergyt~3.925e-5s not39e-5; badkeysnotused. Average/reactiveenergyexchange and gridloss distinct.

---
Tarixiy source qaydlari saqlandi.

# Keyingi: 11-sinf §11–15 — 2026-10-26

281/316,35qolgan.15asl sahifa43–57 tasvirlari/nativehashlari qayta o‘qildi. Source review tayyorgarligi, yangiJSON/runtime hali yo‘q, mustaqil ekspert tasdig‘i emas.

PDF43,44,45,46: Original idealLC energy exchange/Thomsonroot and sample checked. Uniform constantLINEARL/C,Rignored, T=2p sqrt(LC),nu=1/T, conservedW=q²/(2C)+LI²/2. Signedinstantq/I vs peakqm/Im distinct, capacitorplatecharge convention. Quarter-cycleenergyrotation conceptual, no real LC switching task. p3.14 explicitly approximate; exact root/rational round rules. Source46sample T.01256s/20uJ consistent.

PDF46,47,48,49: Original qcos/Ucos/i phasegraphs read. Fix convention I=dq/dt INTO chosenpositiveplate; q=qmcos(theta) then I=-Imsin(theta)=Imcos(theta+pi/2). Source46 prints cos(theta+pi/2)=+sin(theta), wrong sign, while source47 Igraph negative afterqmaximum supports minus. Source48 text says I grows toward negativepeak: |I|/magneticenergy grows, signedI decreases. q/U samephase; current quartershift. Damping energy turnsheat, not disappearance; R-increasesperiod only underdampedmodel beforecritical, not allRstilloscillates. No invented exponential damping formula.

PDF49,50,51,52: Original transistorfeedback/energysource diagram checked. Sustained selfoscillator uses externalDCenergy and phasedfeedback; no perpetualmotion. Source51 180deg is specific inverting-stage/coil convention, not universal totalfeedbackphase; suitable loopfeedback returnsenergy inphase. Transistor not only imaginable possible oscillator switch; no all-mechanical-MHz impossibility assertion. Unsupported universal eachorganresonance/psychologicalhealth claims not included. Conceptual no forced beta/medical/radiation/LLM/newgeneratorruntime.

PDF52,53,54,55: Original pureactiveR sinusoid/phasor/RMS/power1/2 checked. FixedR,pureR,u/i samephase. Pinst=Um*Im*cosPhase² nonnegative and doubledfreq, Pavg=Um*Im/2; RMS=peak/sqrt2 only SINUSOID, not any waveform/universal lightbulb eyes16–20fps myth. Typed providedcos data not generaltrig. Peak/rms mixednotallowed in suppliedgivens. Source55average30W example interprets2A as amplitude, newprompts explicit. ExactirrationalRMS rubrics retain square and SI roundinggrid, not float expectedtruth.

PDF56,57: Original idealcap derivative i=-UmC*omega*sin(theta)=Imcos(theta+pi/2) agrees fixed I=dq/dt convention. Current LEADS voltage90deg in steady sinusoidalidealcap; steadyDC current0aftercharging, not nevertransient. Xc=1/(omegaC)=1/(2pnuC),Im=Um*omegaC. omega rad/s vs nuHz,p3.14 explicit, Xcohms reactive not heatresistor; no claim passivecap dissipatesrmsUI. Source57sample50Hz50uF63.69ohm consistent approximate. No live mains construction.

---
Tarixiy §6–10 qaydlari saqlandi.

# Keyingi: 11-sinf §6–10 — 2026-10-26

276/316,40qolgan.18asl sahifa18–22/27–39 tasvirlari/nativehashlari o‘qildi. Bu source tayyorgarligi; keyingibatch2private draft/runtimehaliyo‘q, independentexpertapproval emas.

PDF18,19,20,21,22: Original images/native hashes checked. Lorentz magnetic force perpendicularv does no work; signedcharge reversesdirection while scalar formulas use MODULUS. Circular R=mv/(|q|B),T=2p*m/(|q|B) only uniform magneticfield/vperpendicularB/nonrelativistic; generalangle force |q|vBsinAlpha. New speeds low vs c, source8.4e7m/s example not asserted relativistically exact. Source21exercise1 radius4cm/B.5 gives2.512mWb not25.12; source22exercise15 v.12m/s*3s=.36m vs given.08m, answer.4A corresponds first, not copied. Source22exercise20 electronperiod8s gives~4.47e-12T not4.5mT (8ns would fit but not guessed/restored).

PDF27,28,29,30: Original Faraday/Lenz diagrams/formulas read. Average Emf=-N*DPhi/Dt over interval; equals instantaneous only constant rate. Flux is per turn, Npositivewhole, normal/looporientation consistent. Lenz opposes CHANGE not alwaysB; open cutring can have inducedvoltage but no closedconductioncurrent, sourceabsolute nointeraction treated approximation. Source30.1A worked value is magnitude; signed DPhi+.005/.2 yieldsEmf-.025,I-.1 in defined orientation. No physical magnet/ring experiments.

PDF30,31,32,33: Original self-induction/henry/solenoid pages checked. For Nturn coil distinguish perturnPhi from LINKAGE Psi=N*Phi=L*I; source31Phi=LI must be interpreted linkage or one-turn, not missingN. ConstantlinearL,Emf=-L*DI/Dt average, signopposescurrentCHANGE not alwayscurrent. L=Emag*dt/DImag only positive magnitudes. LongsolenoidL=mu0*muR*n²*S/l, homogeneous linear core/fixed geometry/endignored, not saturating ferromagnet universal. Same explicit mu01.256e-6 approximate convention. No coil interruption/spark/battery live tests.

PDF33,34,35: Original magneticmaterials ratio B=muR*B0 checked with SAMEcurrent/geometry, not fixedvoltage alone universal comparison. muRpositive dimensionless may <1diamagnet or slightly>1paramagnet; no eps>=1 dielectric guard reused. Ferromagnet response/state/temp/nonlinear saturation matter, not constantmuR onlynature/allfields. Source35example B0.5T/muR60->30T conditional linear algebra not realistic universally unsaturated iron, not used as actual material measurement. Source35 magneticbracelet blood-pressure claim not independently substantiated and not copied into course.

PDF36,37,38,39: Original magneticenergy1/2 and inverse root read. W=LI²/2 for constantLINEARL, work to build field not allsourceenergy(Rloss). Iroot sqrt(2W/L) magnitude; linkageenergy I*Psi/2 sourcePhi clarified. No unsupported B²/(2mu) energy density formula added because not taught here. Source39exercise10 I2.5A/Phi.8mWb gives1mJ not2.5;exercise11L5mH/I.4A gives.4mJ not4;exercise12W60mJ/I3A gives13.333mH not90. Source38.08H*.6A=48mWb not mWatt. New independent numbers and exact root/rounding rules, no homemade electromagnet/fire/razor experiment.

§1–5 review tarixiy qaydlari GRADE10_NEXT_REVIEW.md va SOURCE_REVIEW.md da saqlandi.
