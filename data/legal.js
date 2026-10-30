// "Is it legal in my state?" data. LAST CHECKED: October 29, 2026.
// rec:  "yes" adult-use legal | "partial" possession legal, no licensed stores | "no"
// med:  "full" comprehensive medical program | "limited" low-THC / CBD-only | "none"
// hemp: "ban" state bans or tightly restricts intoxicating hemp THC (delta-8 etc.); listed ONLY where
//       multiple current sources agree | "check" no statewide ban we could confirm (sources disagree
//       or rules are changing). Never mark a state "legal" for hemp THC: the federal rules change
//       Nov 12 and Dec 11, 2026 for every state.
// Sources: Ballotpedia, NORML state laws, MPP, World Population Review / MADD (adult-use list),
// hemp-law trackers cross-checked, Texas DSHS (July 31, 2026 rule).
const LEGAL_CHECKED = "October 29, 2026";
const LEGAL = {
 al:{n:"Alabama",rec:"no",med:"full",hemp:"check",note:"Medical program licensed; recreational use is illegal."},
 ak:{n:"Alaska",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2014; licensed stores statewide."},
 az:{n:"Arizona",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2020 (Prop 207)."},
 ar:{n:"Arkansas",rec:"no",med:"full",hemp:"check",note:"Medical legal since 2016; recreational measures have failed at the ballot. The state's hemp-THC ban has been tied up in court."},
 ca:{n:"California",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2016; the country's biggest licensed market."},
 co:{n:"Colorado",rec:"yes",med:"full",hemp:"ban",note:"Adult-use legal since 2012. Chemically converted cannabinoids like delta-8 are not allowed in hemp products."},
 ct:{n:"Connecticut",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal; high-potency hemp products are limited to licensed cannabis stores."},
 de:{n:"Delaware",rec:"yes",med:"full",hemp:"ban",note:"Adult-use legal; licensed sales began in 2025."},
 dc:{n:"Washington, D.C.",rec:"partial",med:"full",hemp:"check",note:"Possession and gifting are legal, but Congress still blocks licensed recreational sales."},
 fl:{n:"Florida",rec:"no",med:"full",hemp:"check",note:"Large medical program. Recreational amendments fell short; new legalization amendments are aimed at 2028."},
 ga:{n:"Georgia",rec:"no",med:"limited",hemp:"check",note:"Low-THC oil program only; no smokable medical or recreational market."},
 hi:{n:"Hawaii",rec:"no",med:"full",hemp:"check",note:"Medical legal and small amounts decriminalized; recreational bills keep stalling."},
 id:{n:"Idaho",rec:"no",med:"none",hemp:"ban",note:"Fully illegal, including any THC in hemp products. HJR 4 on the Nov 3, 2026 ballot would stop citizens from ever legalizing by initiative."},
 il:{n:"Illinois",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2020; licensed stores statewide. From Nov 12, hemp products over 0.4 mg total THC per container count as cannabis under Illinois law and come off regular store shelves."},
 in:{n:"Indiana",rec:"no",med:"limited",hemp:"check",note:"Low-THC CBD only; recreational and medical bills have not passed."},
 ia:{n:"Iowa",rec:"no",med:"limited",hemp:"ban",note:"Limited medical cannabidiol program. State law sharply limits THC in hemp products."},
 ks:{n:"Kansas",rec:"no",med:"none",hemp:"check",note:"No medical or recreational program; among the strictest states."},
 ky:{n:"Kentucky",rec:"no",med:"full",hemp:"check",note:"Medical program launched in 2025; recreational is illegal. Hemp-derived THC is regulated by the state."},
 la:{n:"Louisiana",rec:"no",med:"full",hemp:"check",note:"Medical legal and expanding; small amounts decriminalized."},
 me:{n:"Maine",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2016. A repeal campaign failed to make the 2026 ballot."},
 md:{n:"Maryland",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2023; sales of $917 million so far in 2026."},
 ma:{n:"Massachusetts",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2016, but Question 8 on the Nov 3, 2026 ballot would end recreational sales (starting 2028 if it passes)."},
 mi:{n:"Michigan",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2018; one of the biggest markets."},
 mn:{n:"Minnesota",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2023; low-dose hemp THC edibles and drinks are regulated and sold to adults 21+."},
 ms:{n:"Mississippi",rec:"no",med:"full",hemp:"ban",note:"Medical program active since 2022; recreational is illegal."},
 mo:{n:"Missouri",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2022. From Nov 12, intoxicating hemp products move into licensed marijuana dispensaries; hemp THC drinks get until Dec 11."},
 mt:{n:"Montana",rec:"yes",med:"full",hemp:"ban",note:"Adult-use legal since 2021."},
 ne:{n:"Nebraska",rec:"no",med:"full",hemp:"check",note:"Voters approved medical cannabis in 2024; the rollout has been slow and contested. Recreational is illegal."},
 nv:{n:"Nevada",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2016; consumption lounges are open."},
 nh:{n:"New Hampshire",rec:"no",med:"full",hemp:"check",note:"Medical only; the last New England state without recreational."},
 nj:{n:"New Jersey",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2022. After Nov 13, hemp THC drinks can only be sold by licensed cannabis retailers. A bill to move that to Dec 11 passed the state Senate; the Assembly has not voted yet."},
 nm:{n:"New Mexico",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2022."},
 ny:{n:"New York",rec:"yes",med:"full",hemp:"ban",note:"Adult-use legal; retail sales passed $4.1 billion. Delta-8 is not allowed in hemp products."},
 nc:{n:"North Carolina",rec:"no",med:"limited",hemp:"check",note:"No comprehensive medical program; hemp-derived products are widely sold."},
 nd:{n:"North Dakota",rec:"no",med:"full",hemp:"ban",note:"Medical legal; recreational measures have failed three times."},
 oh:{n:"Ohio",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2023. New limits took effect in 2026 (90% THC cap on concentrates, 1 oz per flower package)."},
 ok:{n:"Oklahoma",rec:"no",med:"full",hemp:"check",note:"One of the largest medical programs per person; recreational failed in 2023."},
 or:{n:"Oregon",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2014; intoxicating hemp products are limited by state rules."},
 pa:{n:"Pennsylvania",rec:"no",med:"full",hemp:"check",note:"Large medical program; leaders say recreational needs national direction first."},
 ri:{n:"Rhode Island",rec:"yes",med:"full",hemp:"ban",note:"Adult-use legal since 2022. Hemp shops must report their inventory by Dec 4; after Dec 11, over-limit products can be held but not sold."},
 sc:{n:"South Carolina",rec:"no",med:"limited",hemp:"check",note:"CBD only; medical bills keep dying in the legislature."},
 sd:{n:"South Dakota",rec:"no",med:"full",hemp:"check",note:"Medical legal; the 2020 recreational win was struck down in court."},
 tn:{n:"Tennessee",rec:"no",med:"limited",hemp:"check",note:"No medical program beyond limited CBD; hemp-derived THC is regulated for adults 21+."},
 tx:{n:"Texas",rec:"no",med:"limited",hemp:"ban",note:"Since July 31, 2026, delta-8, delta-10, THCP and THCA flower are Schedule I; possession can be a state jail felony. Delta-9 hemp under 0.3% (most gummies and THC drinks) is still sold. Low-THC medical (TCUP) only. Houston votes on Proposition A Nov 3."},
 ut:{n:"Utah",rec:"no",med:"full",hemp:"check",note:"Medical program active; recreational is illegal."},
 vt:{n:"Vermont",rec:"yes",med:"full",hemp:"ban",note:"Adult-use legal; retail since 2022."},
 va:{n:"Virginia",rec:"partial",med:"full",hemp:"check",note:"Possession and home grow are legal for adults; licensed recreational stores are not open yet."},
 wa:{n:"Washington",rec:"yes",med:"full",hemp:"check",note:"Adult-use legal since 2012; intoxicating hemp products must go through licensed cannabis stores."},
 wv:{n:"West Virginia",rec:"no",med:"full",hemp:"check",note:"Medical program active; recreational is illegal."},
 wi:{n:"Wisconsin",rec:"no",med:"limited",hemp:"check",note:"CBD only, though surrounded by legal states."},
 wy:{n:"Wyoming",rec:"no",med:"limited",hemp:"check",note:"CBD only; among the last states with no real program."}
};
