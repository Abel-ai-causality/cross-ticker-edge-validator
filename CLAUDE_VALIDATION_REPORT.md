# PuppyGraph Edge Validation Report (Claude Sonnet 4.6)

**Test Date**: 2026-04-23
**Tool**: `edge_validator_balanced.py` (balanced v3 with specific business reasoning)
**LLM**: `anthropic/claude-sonnet-4-6` (via OpenRouter)
**Environment**: PuppyGraph Production
**Field**: `volume` (trading volume)
**Scope**: Top 20 unique incoming edges per ticker (DISTINCT deduplication)

---

## Overall Statistics

| Ticker | Total | KEEP | MODIFY | REMOVE | ERROR | UNKNOWN |
|--------|-------|------|--------|--------|-------|---------|
| **NVDA** | 20 | 3 (15%) | 2 (10%) | 15 (75%) | 0 (0%) | 0 (0%) |
| **GOOGL** | 20 | 0 (0%) | 1 (5%) | 19 (95%) | 0 (0%) | 0 (0%) |
| **MSFT** | 20 | 0 (0%) | 0 (0%) | 20 (100%) | 0 (0%) | 0 (0%) |
| **TSLA** | 20 | 0 (0%) | 0 (0%) | 20 (100%) | 0 (0%) | 0 (0%) |
| **AAPL** | 20 | 0 (0%) | 1 (5%) | 19 (95%) | 0 (0%) | 0 (0%) |
| **AMZN** | 20 | 0 (0%) | 3 (15%) | 17 (85%) | 0 (0%) | 0 (0%) |
| **TOTAL** | **120** | **3 (2%)** | **7 (5%)** | **110 (91%)** | **0 (0%)** | **0 (0%)** |

---

## NVDA (Total: 20 edges)

**Distribution**: 
✅ KEEP: 3, ⚠️ MODIFY: 2, ❌ REMOVE: 15

### ✅ KEEP (3 edges)

| Source | Confidence | Specific Business Reasoning |
|--------|------------|------------------------------|
| **NTNX** | 62% | Nutanix (NTNX) develops hyperconverged infrastructure (HCI) software and cloud platforms that run on GPU-accelerated hardware nodes, with NVIDIA GPUs increasingly integrated into Nutanix clusters for AI/ML workloads. Nutanix has a direct technology partnership with NVIDIA (including support for NVID. |
| **GOOGL** | 82% | Google (Alphabet) operates Google Cloud Platform and DeepMind, which are among the largest purchasers of NVIDIA H100/A100 GPUs for AI training and inference workloads, with Google reportedly spending billions annually on NVIDIA hardware for its AI infrastructure. The transmission channel is direct:. |
| **ENTG** | 85% | Entegris (ENTG) is a specialty materials company that supplies ultra-high-purity chemicals, advanced materials, and contamination control solutions critical to semiconductor fabrication processes used by TSMC, Samsung, and other foundries that manufacture NVIDIA's GPUs. The exact transmission channe. |

### ⚠️ MODIFY (2 edges)

| Source | Confidence | Specific Business Reasoning |
|--------|------------|------------------------------|
| **QUBT** | 35% | Quantum Computing Inc. (QUBT) develops quantum computing hardware and software, while NVIDIA develops GPUs used extensively in AI/ML workloads and increasingly in quantum-classical hybrid computing research. The relationship is indirect: both QUBT and NVDA are speculative plays on next-generation co. |
| **NXPI** | 45% | NXP Semiconductors (NXPI) designs and sells mixed-signal semiconductors primarily for automotive, IoT, mobile, and industrial markets, while NVIDIA designs high-performance GPUs and AI accelerators for datacenter, gaming, and automotive applications. Both companies compete in the automotive semicond. |

### ❌ REMOVE (15 edges)

| Source | Confidence | Specific Business Reasoning |
|--------|------------|------------------------------|
| **MOFG** | 95% | MOFG (MidWestOne Financial Group) is a small regional community bank headquartered in Iowa, providing retail/commercial banking services to Midwest customers, while NVIDIA designs high-performance GPUs and AI accelerators for datacenter, gaming, and automotive markets. There is no identifiable suppl. |
| **BEAM** | 85% | Beam Therapeutics is a clinical-stage biotechnology company developing base-editing gene therapies with no significant commercial products, while NVIDIA designs high-performance GPUs and AI accelerators for datacenter, gaming, and automotive markets. There is no identifiable supply chain, customer,. |
| **TWI** | 90% | TWI (Titan International) manufactures steel wheels, tires, and undercarriage systems for agricultural tractors, combines, and earthmoving equipment, while NVIDIA designs high-performance GPUs and AI accelerators for datacenter, gaming, and automotive markets. There is no supply chain relationship,. |
| **XEL** | 85% | Xcel Energy (XEL) is a regulated electric and natural gas utility serving customers in the Midwest and Southwest United States, with no direct business relationship to NVIDIA's GPU/AI semiconductor business. While there is an emerging narrative that AI data centers (which use NVIDIA GPUs) consume si. |
| **ETSY** | 85% | Etsy operates an e-commerce marketplace for handmade and vintage goods, connecting independent artisan sellers with consumers, while NVIDIA designs high-performance GPUs for AI/ML training, gaming, and datacenter workloads. There is no direct supply chain, competitive, or customer relationship betwe. |
| **LHX** | 72% | LHX (L3Harris Technologies) is a defense electronics and communications systems company primarily serving military/government customers with products like tactical radios, night vision systems, and ISR platforms. NVDA (NVIDIA) designs high-performance GPUs and AI accelerators for datacenter, gaming,. |
| **JKHY** | 85% | Jack Henry & Associates (JKHY) provides core banking software and payment processing technology specifically to community and mid-tier banks, with no meaningful hardware procurement relationship with NVIDIA. NVIDIA's business is centered on GPU sales to hyperscalers, AI labs, and enterprise data cen. |
| **CL** | 92% | Colgate-Palmolive (CL) is a consumer staples company that manufactures and sells toothpaste, soap, and household cleaning products, while NVIDIA (NVDA) designs high-performance GPUs and AI accelerators for datacenter, gaming, and automotive markets. There is no supply chain relationship, competitive. |
| **ZEUS** | 85% | Olympic Steel (ZEUS) is a metals service center that processes and distributes carbon steel, coated steel, and stainless steel products primarily to industrial manufacturers. NVIDIA designs high-performance GPUs and AI accelerator chips manufactured by TSMC and other semiconductor foundries. There i. |
| **SHEL** | 85% | Shell (SHEL) is a global integrated oil & gas company focused on hydrocarbon exploration, production, refining, and energy trading, while NVIDIA (NVDA) designs high-performance GPUs and AI accelerators for datacenter, gaming, and automotive markets. There is no direct supplier-customer, competitive,. |
| **LITB** | 95% | LightInTheBox (LITB) is a Chinese cross-border e-commerce retailer selling low-cost consumer goods (apparel, gadgets, home goods) primarily to Western consumers via its online marketplace. NVIDIA (NVDA) designs high-performance GPUs for AI/ML training, datacenter computing, and gaming. There is no s. |
| **BAM** | 78% | BAM (Brookfield Asset Management) is an alternative asset manager specializing in real assets — infrastructure, renewable energy, and real estate — with no direct business relationship to NVIDIA's GPU/AI accelerator business. While Brookfield has made thematic moves into AI data center power infrast. |
| **RH** | 90% | RH (RH, formerly Restoration Hardware) is a luxury home furnishings and interior design retailer that sells high-end furniture, lighting, and décor through galleries and catalogs. NVDA (NVIDIA) designs and manufactures GPUs and AI accelerator chips for datacenter, gaming, and automotive markets. The. |
| **Z** | 85% | Zillow Group (Z) operates an online real estate marketplace using AI-powered home valuation tools (Zestimate), while NVIDIA designs high-performance GPUs and AI accelerators for datacenters and enterprise clients. Zillow has no direct procurement relationship with NVIDIA — it consumes cloud compute. |
| **HAFC** | 95% | Hanmi Financial Corporation (HAFC) is a small regional bank headquartered in Los Angeles primarily serving the Korean-American community, offering standard retail/commercial banking services. NVIDIA (NVDA) is a semiconductor company designing high-performance GPUs for AI/ML, gaming, and datacenter a. |

---

## GOOGL (Total: 20 edges)

**Distribution**: 
⚠️ MODIFY: 1, ❌ REMOVE: 19

### ⚠️ MODIFY (1 edges)

| Source | Confidence | Specific Business Reasoning |
|--------|------------|------------------------------|
| **AFRM** | 35% | Affirm (AFRM) operates a Buy Now Pay Later (BNPL) platform that has a partnership with Google Pay/Google Shopping, where Affirm's financing options are integrated into Google's commerce ecosystem, creating a direct but limited business relationship. This integration means that Google Shopping volume. |

### ❌ REMOVE (19 edges)

| Source | Confidence | Specific Business Reasoning |
|--------|------------|------------------------------|
| **VRA** | 92% | Vera Bradley (VRA) is a specialty fashion accessories retailer focused on handbags, luggage, and lifestyle products primarily sold through retail stores and e-commerce. Alphabet/Google (GOOGL) operates Google Search, Google Cloud, YouTube, and Android ecosystem businesses at massive scale. There is. |
| **TFX** | 92% | TFX (Teleflex) is a medical device manufacturer specializing in vascular access, surgical, and respiratory care products (e.g., catheters, laryngoscopes, surgical instruments). GOOGL (Alphabet) operates Google Search, Google Cloud, YouTube, and AI/advertising platforms. There is no direct supply cha. |
| **LMND** | 85% | Lemonade (LMND) is a small AI-driven insurance company (~$1-2B market cap) offering renters, homeowners, and pet insurance, while Alphabet/Google (GOOGL) is a ~$2T diversified technology conglomerate with dominant positions in search, advertising, cloud, and AI. Although Lemonade uses AI/ML in its u. |
| **VFF** | 92% | VFF (Village Farms International) is a Canadian greenhouse produce and cannabis company that grows tomatoes, peppers, cucumbers, and operates cannabis operations under Pure Sunfarms. GOOGL (Alphabet/Google) operates Google Search, YouTube, Google Cloud, and Android — a massive diversified technology. |
| **TGNA** | 82% | TGNA (Tegna Inc.) operates local broadcast television stations and digital media properties across the US, while GOOGL (Alphabet/Google) operates a massive global technology conglomerate spanning search, cloud, advertising, YouTube, and AI. Although Tegna uses Google's advertising technology platfor. |
| **LEVI** | 92% | Levi Strauss & Co. (LEVI) is a denim apparel manufacturer and retailer with business operations centered on clothing design, manufacturing, and retail distribution. Alphabet/Google (GOOGL) operates Google Search, Google Cloud, YouTube, and Android platforms in the digital technology and advertising. |
| **AVNS** | 92% | AVNS (Avanos Medical) is a medical device company specializing in pain management and respiratory health products (e.g., nerve block systems, feeding tubes), while GOOGL (Alphabet) operates Google Search, Google Cloud, YouTube, and AI/ML infrastructure at massive scale. There is no supply chain, cus. |
| **FDP** | 92% | FDP (Fresh Del Monte Produce) is a global producer and distributor of fresh fruits, vegetables, and prepared foods, operating primarily in agricultural commodity markets. Alphabet/Google (GOOGL) operates Google Search, Google Cloud, YouTube, and Android platforms in the digital technology and advert. |
| **WLK** | 90% | WLK (Westlake Corporation) is a petrochemical and building products manufacturer specializing in PVC, chlor-alkali chemicals, and vinyl-based construction materials. GOOGL (Alphabet) operates Google Search, Google Cloud, YouTube, and advertising platforms with no meaningful exposure to petrochemical. |
| **KHC** | 92% | Kraft Heinz (KHC) is a consumer packaged goods company producing food and beverage products (ketchup, cheese, condiments), while Alphabet/Google (GOOGL) operates digital advertising, cloud computing, and AI platforms. There is no direct supply chain, customer, or competitive relationship between KHC. |
| **SMP** | 90% | SMP (Standard Motor Products) manufactures and distributes automotive replacement parts (ignition systems, fuel delivery components, temperature sensors) for the aftermarket auto repair industry. Alphabet/Google operates Google Search, YouTube, Google Cloud, and digital advertising platforms. There. |
| **KDP** | 90% | KDP (Keurig Dr Pepper) is a beverage company that manufactures and distributes coffee, soft drinks, and other beverages, while GOOGL (Alphabet) operates Google Search, Google Cloud, YouTube, and other digital technology platforms. There is no meaningful supply chain, competitive, or customer relatio. |
| **VTOL** | 90% | VTOL (Blade Air Mobility) operates an urban air mobility and helicopter charter service platform, primarily serving short-distance passenger transport in markets like New York and India. Alphabet/Google (GOOGL) operates a massive diversified technology conglomerate including search, cloud computing,. |
| **KMB** | 92% | Kimberly-Clark (KMB) is a consumer staples company manufacturing paper-based household products (Kleenex, Huggies, Scott), while Alphabet/Google (GOOGL) operates a digital advertising platform, cloud computing services, and AI infrastructure. There is no direct supplier-customer, competitive, or sup. |
| **TECK** | 90% | Teck Resources (TECK) is a Canadian diversified mining company primarily producing copper, zinc, steelmaking coal, and other base metals, while Alphabet/Google (GOOGL) operates a global technology conglomerate including search, cloud computing, advertising, and AI infrastructure. Although Google doe. |
| **BNS** | 85% | BNS (Bank of Nova Scotia) is a Canadian multinational banking institution primarily focused on retail banking, wealth management, and capital markets in Canada and Latin America. GOOGL (Alphabet Inc.) operates Google Search, Google Cloud, YouTube, and various AI/technology platforms. There is no dir. |
| **CRS** | 90% | CRS (Carpenter Technology Corporation) is a specialty alloys and high-performance materials manufacturer serving aerospace, defense, medical, and industrial markets. Alphabet/Google (GOOGL) operates digital advertising, cloud computing (Google Cloud), and consumer technology platforms. There is no s. |
| **PLNT** | 90% | Planet Fitness (PLNT) operates a chain of budget fitness centers/gyms with membership-based revenue, while Alphabet/Google (GOOGL) operates a diversified technology conglomerate including search, cloud computing, YouTube, and AI services. There is no direct supplier-customer, competitive, or supply. |
| **TYRA** | 95% | TYRA (Tyra Biosciences) is a small clinical-stage biopharmaceutical company focused on precision oncology drugs targeting FGFR-altered cancers, with no business relationship to Alphabet/Google's core operations in search, advertising, cloud computing, or AI infrastructure. There is no supply chain,. |

---

## MSFT (Total: 20 edges)

**Distribution**: 
❌ REMOVE: 20

### ❌ REMOVE (20 edges)

| Source | Confidence | Specific Business Reasoning |
|--------|------------|------------------------------|
| **NABL** | 78% | N-able (NABL) provides RMM and cybersecurity software exclusively for managed service providers (MSPs), while Microsoft (MSFT) is a $3T diversified technology company spanning cloud, OS, productivity, and enterprise software. Although N-able integrates with Microsoft 365 and Azure within the MSP eco. |
| **DUOL** | 72% | Duolingo (DUOL) is a consumer-facing language learning app that generates revenue primarily through subscriptions and advertising, with no meaningful supply chain or technology dependency on Microsoft. While Microsoft offers competing products (Microsoft Teams language features, LinkedIn Learning, a. |
| **JOUT** | 95% | Johnson Outdoors (JOUT) is a small-cap recreational outdoor equipment manufacturer producing fishing electronics, diving gear, watercraft, and camping equipment, with annual revenues around $600-700M. Microsoft (MSFT) is a $2+ trillion enterprise software, cloud computing, and gaming conglomerate. T. |
| **MXL** | 80% | MaxLinear (MXL) designs semiconductor chips primarily for broadband access, data center interconnects, and storage applications, while Microsoft (MSFT) is a diversified software, cloud, and enterprise services company. Although MSFT operates Azure cloud infrastructure that uses networking hardware,. |
| **AGRO** | 92% | AGRO (Adecoagro S.A.) is a South American agricultural company operating farms, rice mills, and sugar/ethanol facilities primarily in Argentina, Brazil, and Uruguay, while MSFT (Microsoft) is a global technology company focused on cloud computing (Azure), enterprise software, and AI services. There. |
| **GXO** | 72% | GXO Logistics operates as a pure-play contract logistics and warehouse management company, providing outsourced supply chain services (fulfillment centers, automated warehouses) to retailers and manufacturers. Microsoft operates cloud computing (Azure), enterprise software (Office 365, Dynamics), an. |
| **MAT** | 85% | Mattel (MAT) is a toy manufacturer specializing in consumer products like Barbie, Hot Wheels, and Fisher-Price, with revenue driven by retail toy sales and licensing. Microsoft (MSFT) is a diversified technology company with major segments in cloud computing (Azure), enterprise software (Office 365). |
| **LAZ** | 80% | Lazard (LAZ) is a financial advisory and asset management firm specializing in M&A advisory, restructuring, and investment management services, while Microsoft (MSFT) is a diversified technology company focused on cloud computing, software, and AI. Although Lazard may occasionally advise on M&A tran. |
| **QTTB** | 88% | QTTB appears to be a micro-cap or OTC-traded security with no identifiable direct business relationship to Microsoft (a ~$3 trillion enterprise spanning cloud, software, and AI). There is no specific supply chain, competitive, or customer-supplier mechanism linking QTTB's trading activity to MSFT's. |
| **CMP** | 92% | CMP (Compass Minerals) produces road deicing salt, specialty fertilizers (sulfate of potash), and fire retardants from mining operations, while MSFT operates cloud computing (Azure), enterprise software, and AI services. There is zero supply chain, customer, or competitive relationship between a nic. |
| **RDN** | 85% | RDN (Radian Group) is a private mortgage insurance (PMI) company that provides credit risk protection to mortgage lenders, primarily serving the residential housing market. MSFT (Microsoft) operates cloud computing (Azure), enterprise software, gaming, and AI services with no meaningful exposure to. |
| **True** | 85% | "True_volume" is not a recognized stock ticker or standard financial instrument — it appears to be either a synthetic/aggregate variable (e.g., total market volume, a composite index volume metric) or a data artifact. If "True_volume" represents aggregate market-wide trading volume, any relationship. |
| **JOYY** | 85% | JOYY Inc. is a Chinese live-streaming and social media platform (YY Live, Bigo Live) primarily serving Asian markets, while Microsoft is a diversified U.S. technology giant with cloud (Azure), productivity software (Office 365), and gaming businesses. There is no direct supplier-customer, competitiv. |
| **AMT** | 80% | AMT (American Tower Corporation) is a REIT that owns and operates wireless communication tower infrastructure, leasing space to telecom carriers like AT&T, Verizon, and T-Mobile. MSFT (Microsoft) operates Azure cloud, enterprise software, and gaming businesses. While both are large-cap S&P 500 compo. |
| **BFST** | 92% | BFST (Business First Bancshares) is a small regional commercial bank headquartered in Louisiana with ~$3B in assets, focused on local business lending and deposit-taking in the Gulf South region. Microsoft is a global technology giant with ~$3T market cap operating cloud computing (Azure), enterpris. |
| **RCL** | 90% | Royal Caribbean (RCL) is a cruise line operator whose business involves leisure travel, ship operations, and hospitality services, while Microsoft (MSFT) is a diversified technology company focused on cloud computing (Azure), enterprise software, and AI services. Although RCL uses Microsoft cloud/so. |
| **TMC** | 90% | TMC (The Metals Company) is a pre-revenue deep-sea mining startup extracting polymetallic nodules (nickel, cobalt, manganese) targeting EV battery manufacturers and automakers as customers. Microsoft operates cloud computing (Azure), enterprise software, and AI services with no procurement relations. |
| **BP** | 85% | BP is a major integrated oil & gas company focused on hydrocarbon exploration, production, and refining, while MSFT is a diversified technology company operating cloud computing (Azure), enterprise software, and gaming businesses. There is no direct supplier-customer relationship, competitive dynami. |
| **MGNI** | 80% | Magnite (MGNI) is an independent sell-side advertising technology platform specializing in programmatic ad auctions for publishers, while Microsoft (MSFT) is a diversified technology giant spanning cloud computing (Azure), enterprise software (Office 365), gaming (Xbox), and digital advertising (via. |
| **GRBK** | 92% | GRBK (Green Brick Partners) is a residential homebuilder operating primarily in Texas and Georgia, focused on land acquisition, development, and home construction for retail buyers. MSFT (Microsoft) is a global technology conglomerate operating cloud infrastructure (Azure), enterprise software, and. |

---

## TSLA (Total: 20 edges)

**Distribution**: 
❌ REMOVE: 20

### ❌ REMOVE (20 edges)

| Source | Confidence | Specific Business Reasoning |
|--------|------------|------------------------------|
| **DXCM** | 85% | DexCom (DXCM) is a medical device company specializing in continuous glucose monitoring (CGM) systems for diabetes management, while Tesla (TSLA) is an electric vehicle and energy storage manufacturer. There is no direct supply chain, customer, or competitive relationship between these two companies. |
| **HQY** | 92% | HQY (HealthEquity) is a health savings account (HSA) administrator and healthcare financial services company, while TSLA (Tesla) is an electric vehicle manufacturer and energy company. There is no supply chain relationship, competitive dynamic, or customer-supplier link between a healthcare benefits. |
| **FCX** | 80% | FCX (Freeport-McMoRan) is a major copper and gold mining company, while TSLA (Tesla) is an electric vehicle and energy storage manufacturer. Although Tesla is a significant copper consumer (EVs use ~4x more copper than ICE vehicles), the volume co-movement mechanism is too indirect to justify a dire. |
| **BKNG** | 85% | Booking Holdings (BKNG) operates an online travel agency platform (Booking.com, Priceline, Kayak) generating revenue from hotel/flight/rental reservations, while Tesla (TSLA) designs and manufactures electric vehicles and energy storage systems. There is no direct supply chain, customer, or competit. |
| **LC** | 85% | LC (LendingClub) is an online marketplace lending platform focused on personal loans, auto refinancing, and small business loans for retail consumers, while TSLA (Tesla) is an electric vehicle manufacturer and energy company. There is no direct supply chain, customer, or competitive relationship bet. |
| **IQ** | 85% | IQ (iQIYI) is a Chinese online video streaming platform ("Netflix of China") owned by Baidu, focused on entertainment content licensing, original productions, and subscription/advertising revenue in China. TSLA (Tesla) is a US-based electric vehicle and energy storage manufacturer with global operat. |
| **CHWY** | 92% | Chewy (CHWY) is an online pet food and supplies retailer, while Tesla (TSLA) is an electric vehicle and energy storage manufacturer — these businesses operate in entirely unrelated industries with no supply chain, competitive, or customer overlap. There is no plausible transmission channel by which. |
| **AEE** | 82% | AEE (Ameren Corporation) is a regulated electric and gas utility serving Missouri and Illinois, with revenue derived from rate-regulated electricity transmission and distribution. TSLA (Tesla) is an electric vehicle manufacturer and energy storage company. While a superficial connection might be dra. |
| **RNAC** | 95% | RNAC (Rallybio Corporation) is a clinical-stage rare disease biopharmaceutical company focused on maternal-fetal conditions like FNAIT, while TSLA is an electric vehicle and energy storage manufacturer — these businesses share zero supply chain, customer, competitive, or technological overlap. There. |
| **THS** | 90% | TreeHouse Foods (THS) is a private-label packaged food manufacturer specializing in snacks, beverages, and meal solutions sold through grocery retailers, while Tesla (TSLA) is an electric vehicle and energy storage company. There is no supply chain relationship, competitive dynamic, or shared custom. |
| **KB** | 85% | KB (KeyCorp) is a regional U.S. bank headquartered in Cleveland, Ohio, providing retail banking, commercial lending, and financial services to mid-market customers. Tesla (TSLA) is an electric vehicle and clean energy manufacturer with a global supply chain and consumer/enterprise customer base. The. |
| **SSRM** | 90% | SSR Mining (SSRM) is a mid-tier gold and silver mining company focused on precious metals extraction at operations in Turkey, Canada, and Argentina, while Tesla (TSLA) is an electric vehicle and energy storage manufacturer. There is no supply chain relationship between a precious metals miner and an. |
| **FNF** | 85% | FNF (Fidelity National Financial) is a title insurance and real estate transaction services company, primarily serving the residential and commercial real estate market. TSLA (Tesla) is an electric vehicle manufacturer and energy company. There is no direct supply chain, customer, competitive, or fi. |
| **GL** | 90% | GL (Globe Life Inc.) is a life and health insurance company focused on direct-to-consumer insurance products for middle-income Americans, with no meaningful business relationship to Tesla's electric vehicle and energy storage operations. There is no supply chain, competitive, or customer relationshi. |
| **MCY** | 90% | MCY (Mercury General Corporation) is a personal lines property and casualty insurance company focused on auto and home insurance in California and other states. TSLA (Tesla) is an electric vehicle manufacturer and energy company. While Mercury General does write auto insurance policies that may cove. |
| **VIOT** | 90% | VIOT (Viomi Technology) manufactures Chinese smart home appliances (IoT refrigerators, water purifiers, washing machines) within the Xiaomi ecosystem, while TSLA designs and sells electric vehicles, battery storage, and solar products globally. There is no supplier-customer relationship, competitive. |
| **AHH** | 92% | AHH (Armada Hoffler Properties) is a mid-sized REIT focused on mixed-use real estate development and property management in the Mid-Atlantic region, while TSLA (Tesla) is a global electric vehicle and clean energy company. There is no identifiable supply chain, customer, competitive, or financial re. |
| **FINV** | 85% | FinVolution Group operates a Chinese digital consumer lending marketplace with no documented supply chain, competitive, or partnership relationship with Tesla. While both companies have China exposure (Tesla's Shanghai Gigafactory; FinVolution's China-only operations), any co-movement in trading vol. |
| **AGI** | 90% | Alamos Gold (AGI) is a Canadian mid-tier gold mining company focused on gold extraction and production, while Tesla (TSLA) is an EV manufacturer and AI/energy company — these businesses operate in entirely unrelated industries with no supply chain, competitive, or customer relationship. Gold mining. |
| **CTKB** | 95% | Cytek Biosciences (CTKB) develops and sells spectral flow cytometry instruments for life sciences research, while Tesla (TSLA) manufactures electric vehicles, energy storage systems, and autonomous driving technology — two entirely unrelated industries with no supply chain, competitive, or customer-. |

---

## AAPL (Total: 20 edges)

**Distribution**: 
⚠️ MODIFY: 1, ❌ REMOVE: 19

### ⚠️ MODIFY (1 edges)

| Source | Confidence | Specific Business Reasoning |
|--------|------------|------------------------------|
| **KEYS** | 35% | Keysight Technologies (KEYS) designs and manufactures electronic test and measurement equipment, including RF/microwave analyzers, oscilloscopes, and network analyzers used in electronics R&D and manufacturing. Apple (AAPL) is a major consumer electronics company that uses test and measurement equip. |

### ❌ REMOVE (19 edges)

| Source | Confidence | Specific Business Reasoning |
|--------|------------|------------------------------|
| **ZIM** | 85% | ZIM Integrated Shipping Services operates a container shipping line primarily serving trans-Pacific and Asia-Europe trade routes, while Apple designs and sells consumer electronics with manufacturing concentrated in Asia. Although Apple relies on ocean freight to ship finished goods from Chinese/Asi. |
| **SSYS** | 85% | Stratasys (SSYS) is a 3D printing/additive manufacturing company specializing in industrial and professional FDM/PolyJet printers, while Apple (AAPL) is a consumer electronics and software ecosystem company. There is no direct supply chain relationship — Stratasys does not supply 3D printing equipme. |
| **DOCN** | 85% | DigitalOcean (DOCN) is a cloud infrastructure provider targeting small-to-medium businesses and individual developers, offering VPS hosting, managed databases, and Kubernetes services. Apple (AAPL) is a consumer electronics and software ecosystem company whose primary revenue comes from iPhone hardw. |
| **PEBO** | 92% | PEBO (Peoples Bancorp of North Carolina) is a small regional community bank operating primarily in North Carolina, offering standard retail and commercial banking services to local customers. AAPL (Apple Inc.) is a global consumer electronics and software giant with a $3+ trillion market cap. There. |
| **AEIS** | 88% | Advanced Energy Industries (AEIS) manufactures precision power conversion systems sold to semiconductor equipment companies (Applied Materials, Lam Research), placing them 3-4 supply chain steps away from Apple, which sources finished chips from TSMC. There is no direct business relationship between. |
| **KHC** | 92% | Kraft Heinz (KHC) is a consumer packaged food and beverage company producing branded food products (Kraft, Heinz, Oscar Mayer, etc.), while Apple (AAPL) designs and sells consumer electronics, software, and digital services. There is no supply chain relationship, competitive overlap, or direct busin. |
| **MRTN** | 92% | MRTN (Marten Transport) is a long-haul trucking and logistics company operating refrigerated and temperature-sensitive freight transportation across North America, while AAPL (Apple Inc.) is a consumer electronics and software giant focused on iPhones, Macs, and services. There is no direct supply c. |
| **PATH** | 82% | UiPath (PATH) is an enterprise robotic process automation (RPA) software company focused on workflow automation for back-office processes, while Apple (AAPL) is a consumer electronics and software ecosystem company. There is no direct supplier-customer relationship, no competitive overlap, and no sh. |
| **WEC** | 92% | WEC Energy Group is a regulated electric and natural gas utility serving Wisconsin, Illinois, Michigan, and Minnesota, with revenues derived almost entirely from rate-regulated energy delivery to residential and commercial customers. Apple Inc. designs and sells consumer electronics, software, and s. |
| **LDOS** | 85% | Leidos (LDOS) is a defense and government IT services contractor specializing in national security, health, and civil government solutions, while Apple (AAPL) is a consumer electronics and software company. There is no direct supply chain, competitive, or customer relationship between Leidos's gover. |
| **CBSH** | 90% | CBSH (Commerce Bankshares) is a mid-sized regional bank headquartered in Kansas City, Missouri, primarily serving retail and commercial banking customers in the Midwest. AAPL (Apple Inc.) is a global consumer electronics and software company. There is no specific business relationship between Commer. |
| **SLF** | 90% | Sun Life Financial operates as a Canadian life insurance and wealth management company with no direct operational relationship to Apple's consumer electronics or software business. Any co-movement in trading volume would be driven entirely by macro-level institutional flows or broad market sentiment. |
| **RCI** | 72% | Rogers Communications (RCI) is a Canadian telecom carrier that distributes Apple iPhones through its wireless retail network, representing one of three major Canadian carriers selling Apple devices. However, Canada constitutes only ~2-3% of Apple's global revenue, making Rogers' contribution to Appl. |
| **TRIP** | 85% | TripAdvisor (TRIP) operates an online travel review and booking platform, while Apple (AAPL) designs and sells consumer electronics, software, and services. There is no direct supplier-customer, competitive, or supply chain relationship between these two companies — TRIP does not purchase Apple hard. |
| **CNMD** | 90% | CNMD (Cantel Medical/Conmed Corporation) is a medical device company specializing in surgical instruments, orthopedic devices, and endoscopy equipment for healthcare providers. AAPL (Apple Inc.) designs and sells consumer electronics, software, and services including iPhone, Mac, and Apple Watch. Th. |
| **EKSO** | 95% | Ekso Bionics (EKSO) is a small-cap medical robotics company specializing in exoskeleton rehabilitation devices for stroke and spinal cord injury patients, with revenues in the low tens of millions annually. Apple (AAPL) is a $3 trillion consumer electronics and software giant whose volume is driven. |
| **IVVD** | 97% | Invivyd (IVVD) is a small-cap clinical-stage biopharmaceutical company developing monoclonal antibody COVID-19 treatments, while Apple (AAPL) is a mega-cap consumer electronics and software company — these businesses have absolutely no supply chain, competitive, or customer relationship. There is no. |
| **BP** | 90% | BP is a British multinational oil and gas company focused on petroleum exploration, production, refining, and energy transition projects, while Apple is a consumer electronics and software company whose primary products (iPhones, Macs, services) have no meaningful supply chain or revenue dependency. |
| **CHD** | 90% | Church & Dwight (CHD) is a consumer staples company manufacturing household and personal care products (Arm & Hammer, OxiClean, Trojan, Vitafresh), while Apple (AAPL) is a technology hardware/software company producing smartphones, computers, and services. There is no supply chain relationship, comp. |

---

## AMZN (Total: 20 edges)

**Distribution**: 
⚠️ MODIFY: 3, ❌ REMOVE: 17

### ⚠️ MODIFY (3 edges)

| Source | Confidence | Specific Business Reasoning |
|--------|------------|------------------------------|
| **ADBE** | 35% | Adobe (ADBE) provides creative software (Creative Cloud, Document Cloud) and digital experience platforms (Experience Cloud), while Amazon (AMZN) operates AWS cloud infrastructure, e-commerce, and advertising services. There is an indirect relationship: Adobe's Experience Cloud and marketing analyti. |
| **ABNB** | 35% | Airbnb operates a short-term rental marketplace platform, while Amazon operates e-commerce, cloud computing (AWS), and digital advertising businesses. The most plausible indirect link is that both are large-cap consumer/tech platform companies that share institutional investors and are subject to si. |
| **NVDA** | 55% | NVIDIA produces GPUs that are central to AI/ML infrastructure, and Amazon Web Services (AWS) is one of NVIDIA's largest cloud customers, purchasing H100/A100 GPUs to power AWS EC2 instances (e.g., P4, P5 instances) and Amazon Bedrock AI services. The relationship is real but indirect as a causal dri. |

### ❌ REMOVE (17 edges)

| Source | Confidence | Specific Business Reasoning |
|--------|------------|------------------------------|
| **SVRA** | 95% | SVRA (Savara Inc.) is a small clinical-stage biopharmaceutical company focused on rare lung diseases (specifically autoimmune pulmonary alveolar proteinosis), with a market cap in the hundreds of millions range. Amazon (AMZN) is a massive diversified technology and e-commerce conglomerate operating. |
| **SLGN** | 85% | Silgan Holdings (SLGN) is a manufacturer of rigid packaging containers (metal cans, closures, plastic containers) primarily serving consumer staples companies like food and beverage producers. Amazon (AMZN) operates e-commerce, cloud computing (AWS), and digital advertising businesses. While Amazon. |
| **EVRG** | 90% | EVRG (Evergy) is a regulated electric utility serving Kansas and Missouri, generating and distributing electricity to residential and commercial customers in the Midwest. AMZN (Amazon) is a global e-commerce, cloud computing (AWS), and logistics conglomerate. While Amazon does consume electricity at. |
| **SRPT** | 90% | SRPT (Sarepta Therapeutics) is a rare disease biopharmaceutical company focused on Duchenne muscular dystrophy (DMD) gene therapies and RNA-based treatments, while AMZN (Amazon) operates e-commerce, AWS cloud infrastructure, and digital advertising businesses. There is no direct supply chain, custom. |
| **ARE** | 85% | Alexandria Real Estate Equities (ARE) is a REIT specializing in life science and technology office/lab campuses, primarily serving biotech and pharmaceutical tenants. Amazon (AMZN) is a diversified e-commerce, cloud computing (AWS), and digital advertising conglomerate. While Amazon has some real es. |
| **SQM** | 85% | SQM (Sociedad Química y Minera de Chile) is a Chilean mining company that is one of the world's largest producers of lithium, potassium, and specialty plant nutrients, with lithium being its primary growth driver for EV battery supply chains. Amazon (AMZN) operates e-commerce, AWS cloud infrastructu. |
| **NTES** | 80% | NetEase (NTES) is a Chinese internet company primarily focused on online gaming (e.g., titles like Fantasy Westward Journey, Naraka: Bladepoint), music streaming (NetEase Cloud Music), and e-commerce in China. Amazon (AMZN) operates U.S.-centric e-commerce, AWS cloud infrastructure, and digital adve. |
| **IRDM** | 72% | Iridium Communications (IRDM) operates a satellite constellation providing voice and data services primarily to maritime, aviation, and government/military customers, while Amazon (AMZN) operates e-commerce, AWS cloud infrastructure, and advertising businesses. There is no direct supplier-customer,. |
| **ALTO** | 92% | Alto Ingredients (ALTO) is a small-cap specialty ethanol and alcohol producer (~$200M market cap) serving sanitizer, beverage, and industrial markets, while Amazon operates a ~$2T e-commerce, cloud (AWS), and logistics empire. There is no identifiable direct supply chain, customer, or competitive re. |
| **SNAP** | 72% | Snap Inc. operates a social media/messaging platform (Snapchat) focused on ephemeral content and AR filters, while Amazon operates a massive e-commerce, cloud computing (AWS), and digital advertising ecosystem. Although both companies compete marginally in digital advertising (Snap sells social medi. |
| **FIS** | 72% | FIS (Fidelity National Information Services) provides payment processing, banking technology, and financial software solutions primarily to financial institutions and merchants. AMZN operates e-commerce, cloud computing (AWS), and digital advertising businesses. While FIS processes payments that may. |
| **KIM** | 82% | Kimco Realty (KIM) is a REIT specializing in open-air shopping centers anchored by grocery and discount retailers, while Amazon (AMZN) is a diversified e-commerce, cloud computing, and logistics giant. The purported causal link is superficially plausible only in that Amazon's e-commerce growth has h. |
| **WGO** | 85% | WGO (Winnebago Industries) manufactures recreational vehicles (RVs) and marine products, while AMZN operates e-commerce, cloud computing (AWS), and digital advertising businesses. There is no direct supply chain relationship — Winnebago does not rely on Amazon Web Services as a critical infrastructu. |
| **BRO** | 85% | Brown & Brown (BRO) is a mid-sized insurance brokerage firm that distributes property, casualty, and employee benefits insurance products to businesses and individuals. Amazon (AMZN) operates e-commerce, cloud computing (AWS), advertising, and logistics businesses at massive scale. There is no direc. |
| **LTH** | 88% | Life Time Group Holdings operates premium brick-and-mortar fitness clubs generating revenue through in-person memberships and services, while Amazon operates e-commerce, AWS cloud, and Prime subscription businesses at massive scale. There is no direct supplier-customer relationship, competitive dyna. |
| **BLNK** | 85% | Blink Charging (BLNK) operates a network of EV charging stations primarily serving residential and commercial customers, while Amazon (AMZN) is a massive e-commerce, cloud computing, and logistics conglomerate. Although Amazon has invested in EV infrastructure for its delivery fleet (notably through. |
| **AMN** | 85% | AMN Healthcare Services (AMN) is a healthcare staffing and workforce solutions company that places nurses, physicians, and allied health professionals in hospitals and healthcare facilities. Amazon (AMZN) is a diversified e-commerce, cloud computing (AWS), and digital advertising conglomerate. There. |

---

## Methodology

### LLM Configuration
- **Model**: `anthropic/claude-sonnet-4-6` (Claude Sonnet 4.6)
- **Provider**: OpenRouter (with forced Anthropic routing)
- **Temperature**: 0.1 (deterministic)
- **Max tokens**: 800 (for detailed reasoning)

### Prompt Design (Balanced v3)

The v3 prompt explicitly requires **specific business-level reasoning**:

- **Forbidden vague reasonings**: "same sector", "market correlation", "tech company"
- **Required specificity**: Each reasoning must include:
  1. What each company **specifically** does (e.g., 'GOOGL operates Google Cloud Platform providing AI/ML infrastructure')
  2. The **exact nature** of their relationship (e.g., 'GOOGL purchases NVIDIA GPUs for AI training clusters')
  3. **Why** this would cause volume co-movement (e.g., 'GOOGL AI capacity announcements drive GPU orders')

### Verdict Definitions
- **KEEP**: Concrete, quantifiable business relationship (supplier/customer/competitor/supply chain)
- **MODIFY**: Indirect link (sector effect, shared macro, ETF co-holding) — exists but doesn't justify full causal edge
- **REMOVE**: No identifiable business relationship — likely statistical noise

### Graph Query
```cypher
MATCH (source)-[r:CAUSES]->(target)
WHERE target.node_name = '{TICKER}_volume'
RETURN DISTINCT source.node_name, target.node_name
LIMIT 20
```

## Usage

```bash
# Prerequisites
export OPENROUTER_API_KEY="sk-or-v1-..."
export PUPPYGRAPH_PROD_PASSWORD="..."

# Run validation
python3 edge_validator_balanced.py NVDA \
  --field volume \
  --mode in \
  --top 20 \
  --env prod \
  --model anthropic/claude-sonnet-4-6
```

---

*Report generated: 2026-04-23 via edge_validator_balanced.py*