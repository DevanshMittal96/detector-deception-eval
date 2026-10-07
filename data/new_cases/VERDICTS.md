# Tapestry verdicts: new edge cases (run 2026-10-07)

Source: `data/new_cases/tapestries/` (19 tapestries + `detections.json`, τ = 0.50).
Each tapestry was inspected visually; every score below is copied from `detections.json`.
Model order: DETR, SSD, FCOS, Faster R-CNN, RetinaNet, Mask R-CNN, YOLO v11.
WEAK = fewer than 2 of 7 models make the intended error.

**Input-format note.** The JSON keys are `.avif` files for 18 of 19 images (only statue4 is `.jpg`), while the README lists `.jpg` originals. If the AVIF files are recompressed copies, this may explain some differences from the README numbers.

## Summary

| Case | Intended error | Fooled k/7 | Models |
|---|---|---|---|
| statue1_pick | person on bronze statue | 7/7 | all 7 |
| statue2_pick | horse/person on bronze horse and two bronze men | 7/7 | all 7 |
| statue3_pick | person (or animal) on abstract statues | **1/7 WEAK** | SSD (other 3 models put *fire hydrant* on the statues) |
| statue4_pick | animal class on embracing-couple statue | 7/7 | all 7 (elephant) |
| animalstatue_pick | live animal on deer sculptures | 5/7 | DETR, FCOS, Faster, Mask, YOLO (horse) |
| animalstatue_alt1 | live animal on stag statue | 5/7 | SSD (cow), FCOS, Faster, Mask, YOLO (bird) |
| scarecrow_pick | person on scarecrow | 6/7 | DETR, FCOS, Faster, RetinaNet, Mask, YOLO |
| billboard3d_pick | animal class on screen cat | 6/7 | DETR, FCOS, Faster, RetinaNet, Mask, YOLO |
| billboard3d_alt1 | animal class on screen cat | 5/7 | DETR, FCOS, Faster, RetinaNet, Mask |
| busad_pick | person on printed model | 5/7 | DETR, SSD, Faster, RetinaNet, Mask |
| buswrap_pick | potted plant on livery / bus missed | 4/7 (bus missed); 0/7 potted plant on livery | SSD, FCOS, RetinaNet, YOLO miss the bus. The potted-plant boxes are on **real** shrubs in a roadside planter |
| carrier_pick | separate car boxes on carried cars | 3/7 | FCOS, Faster, Mask |
| carrier_alt1 | separate car/truck boxes on carried vehicles | 7/7 | all 7 |
| mobilityscooter_pick | scooter forced into a COCO class or missed | 7/7 | 6 say motorcycle; YOLO misses the scooter and rider |
| rickshaw_pick | cart forced into a COCO class or missed | 7/7 | 6 give a wrong class; RetinaNet misses the cart |
| cargotrike_pick | mattress load → truck | 4/7 | SSD, FCOS, Faster, Mask |
| headload_pick | head load → wrong class | 5/7 | DETR, FCOS, Faster, Mask, YOLO |
| horsecart_pick | horses → wrong animal class, or missed | 4/7 | Faster, RetinaNet, Mask (cow), YOLO (elephant) |
| glare_pick | phantom classes from glare | **0/7 WEAK** | none (person boxes fall on the real driver and passenger) |

**Differences from the README's "Cases that reproduce" table**
- statue3: README 7/7 with elephant. Now no elephant, and the only person boxes on the statues are SSD's. The other "person" boxes are three real distant pedestrians at the left edge.
- buswrap: the README says "plants on the livery". In the tapestry the plants are real shrubs in a concrete planter in front of the bus, plus a real palm. The livery is a dark wrap with Chinese text. Only "bus missed" (4/7) holds up.
- carrier_pick: README 6/7. Only 3/7 put a car box on a carried car. The many small car boxes in DETR, RetinaNet and others are on real distant traffic.
- glare: README listed airplane, cup and car. This run produces no airplane or cup.
- horsecart: SSD now detects a horse (0.57). README said "SSD finds nothing".
- busad: 5/7 rather than 4/7. animalstatue_alt1: 5/7 if SSD's cow counts. mobilityscooter and rickshaw: 7/7 when "missed" counts as the intended error.

---

## 1. statue1_pick (55iRnWQqcFA): bronze man on a snowy path

| Model | Error | Label + score on the statue |
|---|---|---|
| DETR | Y | person 1.00 |
| SSD | Y | person 0.97 |
| FCOS | Y | person 0.85 |
| Faster R-CNN | Y | person 0.98 |
| RetinaNet | Y | person 0.90 |
| Mask R-CNN | Y | person 0.98 |
| YOLO v11 | Y | person 0.93 |

**Fooled: 7/7** (all). The other person boxes, 0.63 to 1.00, are on two to four real pedestrians in the background, so they are correct.
Other errors: FCOS boat 0.54 on the waste bin at the left edge.
**Caption:** A life-size bronze statue of a man stands beside a snowy footpath. All seven detectors label the statue "person", with scores from 0.85 (FCOS) to 1.00 (DETR), and give it a box as large as the real pedestrians in the background.

## 2. statue2_pick (0lFkwv-g7Rg): bronze horse and two bronze men among parked cars

| Model | Error | Labels on the statues |
|---|---|---|
| DETR | Y | horse 1.00; person 1.00, 1.00 |
| SSD | Y | horse 0.89; person 0.59 |
| FCOS | Y | horse 0.66, cow 0.59; person 0.83, 0.67 |
| Faster R-CNN | Y | horse 0.97, cow 0.81; person 0.95, 0.93 |
| RetinaNet | Y | horse 0.83; person 0.74, 0.61 |
| Mask R-CNN | Y | horse 0.79, cow 0.82; person 1.00, 0.98 |
| YOLO v11 | Y | horse 0.95; person 0.76, 0.69 |

**Fooled: 7/7** (all).
Other errors: the horse statue also gets "cow" from FCOS (0.59), Faster R-CNN (0.81) and Mask R-CNN (0.82). Chair from DETR (0.52) and Mask R-CNN (0.72) on background structures. Handbag from Mask R-CNN (0.55). The car boxes are on real parked cars.
**Caption:** A bronze horse and two bronze men stand next to a road with parked cars. Every detector reports a horse (0.66 to 1.00) and at least one person (0.59 to 1.00) on the statues. Three models also label the horse statue "cow" (up to 0.82, Mask R-CNN).

## 3. statue3_pick (TNtkDMuUJ2A): abstract figurative statues in a shopping street (WEAK)

| Model | Error | Labels on the statues |
|---|---|---|
| DETR | N | none (its 3 person boxes are on real distant pedestrians) |
| SSD | Y | person 0.80, 0.72 |
| FCOS | N (fire hydrant) | fire hydrant 0.64, 0.59 |
| Faster R-CNN | N (fire hydrant) | fire hydrant 0.90, 0.62, 0.54 |
| RetinaNet | N | none |
| Mask R-CNN | N (fire hydrant) | fire hydrant 0.78, 0.66 |
| YOLO v11 | N | none |

**Fooled: 1/7 (SSD). WEAK.** If any false object class on the statues counts, the total is 4/7 (SSD, FCOS, Faster R-CNN, Mask R-CNN). No elephant appears in this run.
Other notes: the person boxes from DETR, FCOS, Faster, RetinaNet, Mask and YOLO (0.70 to 1.00) are all on three real pedestrians far down the street.
**Caption:** Three abstract, roughly human-shaped bronze statues stand in a pedestrian street. Only SSD labels them "person" (0.80, 0.72). FCOS, Faster R-CNN and Mask R-CNN label them "fire hydrant" (up to 0.90), and the other three models report nothing on the statues.

## 4. statue4_pick (XXttrfPd9dg): bronze embracing couple

| Model | Error | Label on the statue |
|---|---|---|
| DETR | Y | elephant 0.78 |
| SSD | Y | elephant 1.00 |
| FCOS | Y | elephant 0.67 |
| Faster R-CNN | Y | elephant 0.91 |
| RetinaNet | Y | elephant 0.79 |
| Mask R-CNN | Y | elephant 0.94 |
| YOLO v11 | Y | elephant 0.87 |

**Fooled: 7/7** (all). No model labels the statue "person".
Other errors: DETR person 0.68 on a wooden garden chair at the right, plus bench 0.86 and 0.50. The small person boxes from DETR, FCOS, Faster and Mask (0.52 to 0.98) are on real people across the pond.
**Caption:** A dark bronze sculpture of two embracing figures fills the frame. All seven detectors label it "elephant", from 0.67 (FCOS) to 1.00 (SSD), and none labels it "person".

## 5. animalstatue_pick (5_k5BTl8qdU): two deer sculptures on a coastal hill

| Model | Error | Labels on the sculptures |
|---|---|---|
| DETR | Y | horse 1.00, 0.98 |
| SSD | N | none |
| FCOS | Y | horse 0.75, 0.68 |
| Faster R-CNN | Y | horse 0.90, 0.84 |
| RetinaNet | N | none |
| Mask R-CNN | Y | horse 0.83, 0.73 |
| YOLO v11 | Y | horse 0.78, 0.65 |

**Fooled: 5/7** (DETR, FCOS, Faster R-CNN, Mask R-CNN, YOLO v11). Other errors: none.
**Caption:** Two metal deer sculptures stand on a grassy headland. Five of seven detectors report two live horses, from 0.65 (YOLO v11) to 1.00 (DETR). SSD and RetinaNet report nothing.

## 6. animalstatue_alt1 (oYzDMgy3gA8): stag statue against the sky

| Model | Error | Label on the statue |
|---|---|---|
| DETR | N | none |
| SSD | Y | cow 0.59 |
| FCOS | Y | bird 0.67 |
| Faster R-CNN | Y | bird 0.98 |
| RetinaNet | N | none |
| Mask R-CNN | Y | bird 0.93 |
| YOLO v11 | Y | bird 0.85 |

**Fooled: 5/7** (SSD, FCOS, Faster R-CNN, Mask R-CNN, YOLO v11). Without SSD's cow, the bird count is 4/7. Other errors: none.
**Caption:** A verdigris stag statue on a rock is seen against a clear sky. Four detectors label it "bird" (0.67 to 0.98, the highest from Faster R-CNN) and SSD labels it "cow" (0.59). DETR and RetinaNet report nothing.

## 7. scarecrow_pick (N5gmXhvh5Ok): decorative scarecrow

| Model | Error | Label on the scarecrow |
|---|---|---|
| DETR | Y | person 0.96 |
| SSD | N | teddy bear 0.91 |
| FCOS | Y | person 0.84 |
| Faster R-CNN | Y | person 0.99 |
| RetinaNet | Y | person 0.95 |
| Mask R-CNN | Y | person 0.97 |
| YOLO v11 | Y | person 0.87 |

**Fooled: 6/7** (all except SSD).
Other errors: FCOS person 0.50 on a white garden chair in the background. Faster R-CNN umbrella 0.60, a small box in the background.
**Caption:** A straw-stuffed scarecrow with a painted face stands beside a road. Six detectors label it "person", from 0.84 (FCOS) to 0.99 (Faster R-CNN), while SSD labels it "teddy bear" (0.91).

## 8. billboard3d_pick (3phw04dIstk): 3D cat billboard, Shinjuku

| Model | Error | Labels on the screen cat |
|---|---|---|
| DETR | Y | bird 0.93 |
| SSD | N | none |
| FCOS | Y | cat 0.56, dog 0.54, bird 0.54 |
| Faster R-CNN | Y | bird 0.80, cat 0.68 |
| RetinaNet | Y | cat 0.67 |
| Mask R-CNN | Y | cat 0.71 |
| YOLO v11 | Y | bird 0.83 |

**Fooled: 6/7** (all except SSD). The many person boxes are on real pedestrians.
Other notes: at street level, Faster R-CNN reports truck 0.63 and Mask R-CNN reports truck 0.62 and refrigerator 0.62. The refrigerator box is on a white hoarding at the right. Faster R-CNN stop sign 0.75 is a small street-level box that cannot be checked at tapestry resolution.
**Caption:** A large anamorphic screen above a Tokyo street shows a calico cat. Six of seven detectors place an animal box on the screen: "cat" (up to 0.71, Mask R-CNN), "bird" (up to 0.93, DETR) or, from FCOS, cat, dog and bird together (0.54 to 0.56). SSD reports nothing on the screen.

## 9. billboard3d_alt1 (Bz3QUd7X_oQ): 3D cat billboard above a crowded crossing

| Model | Error | Labels on the screen cat |
|---|---|---|
| DETR | Y | cat 1.00 |
| SSD | N | none |
| FCOS | Y | cat 0.60 |
| Faster R-CNN | Y | cat 0.96 |
| RetinaNet | Y | cat 0.83 |
| Mask R-CNN | Y | cat 0.75, dog 0.53 |
| YOLO v11 | N | none |

**Fooled: 5/7** (DETR, FCOS, Faster R-CNN, RetinaNet, Mask R-CNN).
Other errors: the rendered props on the screen are also detected: cup from DETR (0.68) and Faster R-CNN (0.92), and bottle from Faster R-CNN (0.69). A small red sign is labelled stop sign by FCOS (0.54), Faster R-CNN (0.77) and Mask R-CNN (0.82); its true type cannot be checked at this resolution. Person and handbag boxes are on the real crowd.
**Caption:** A 3D screen above a busy crossing shows a giant calico cat. Five detectors report a "cat" on the screen, from 0.60 (FCOS) to 1.00 (DETR), and two also label the rendered cup as a real "cup" (up to 0.92, Faster R-CNN). SSD and YOLO v11 report nothing on the screen.

## 10. busad_pick (hg91qNY26Bc): double-decker bus with a printed model

| Model | Error | Label on the printed model |
|---|---|---|
| DETR | Y | person 1.00 |
| SSD | Y | person 0.60 |
| FCOS | N | none |
| Faster R-CNN | Y | person 0.94 |
| RetinaNet | Y | person 0.66 |
| Mask R-CNN | Y | person 0.96 |
| YOLO v11 | N | none |

**Fooled: 5/7** (DETR, SSD, Faster R-CNN, RetinaNet, Mask R-CNN).
Other notes: Faster R-CNN (0.70), RetinaNet (0.60) and Mask R-CNN (0.66) put a duplicate "truck" box on the partly visible bus at the left. Several small person boxes (0.50 to 0.87) sit at window level on the buses; they may be passengers, which cannot be checked at tapestry resolution. Every model finds the bus itself (0.84 to 1.00).
**Caption:** A double-decker bus carries a large printed advertisement of a woman holding a phone. Five of seven detectors label the printed figure "person", from 0.60 (SSD) to 1.00 (DETR). FCOS and YOLO v11 detect only the bus.

## 11. buswrap_pick (BwXpSrzhBFs): dark-wrapped bus behind a roadside planter

| Model | Bus missed? | Potted plant on livery? | Detections |
|---|---|---|---|
| DETR | N (bus 0.78) | N | potted plant 0.99, 0.97, 0.74, 0.72, 0.57 on real shrubs; truck 0.98 and car 0.75 on the real black car |
| SSD | **Y** | N | nothing |
| FCOS | **Y** | N | nothing |
| Faster R-CNN | N (bus 0.57) | N | potted plant 0.66, 0.55, 0.51 on shrubs; potted plant 0.53 on the real palm |
| RetinaNet | **Y** | N | potted plant 0.52 on a shrub |
| Mask R-CNN | N (bus 0.78) | N | potted plant 0.82, 0.54 on shrubs |
| YOLO v11 | **Y** | N | nothing |

**Fooled: 4/7 for "bus missed"** (SSD, FCOS, RetinaNet, YOLO v11); **0/7 for "potted plant on the livery".**
Check: in the Original panel the plants are real shrubs in a concrete roadside planter in front of the bus, and the palm is a real plant in front of a shopfront. The livery is a black wrap with large Chinese text and no plant graphics, so the potted-plant boxes are not mimicry errors. SSD, FCOS and YOLO also miss the black car in front of the bus.
**Caption:** A double-decker bus with a dark, text-covered wrap passes behind a planted median. Four of seven detectors (SSD, FCOS, RetinaNet, YOLO v11) do not detect the bus, and three detect it with moderate confidence (0.57 to 0.78). The potted-plant boxes fall on the real shrubs in front of it.
*Recommendation:* reframe this case as "dark bus wrap → missed vehicle" or drop it. The potted-plant claim is not supported.

## 12. carrier_pick (9iTgJ8mv_S4): car transporter on a highway

| Model | Error | Boxes on the carrier and its load |
|---|---|---|
| DETR | N | truck 1.00 (whole rig) |
| SSD | N | truck 0.93 (whole rig) |
| FCOS | Y | car 0.76 (upper carried car), car 0.60 (lower load), motorcycle 0.53 (rig) |
| Faster R-CNN | Y | car 0.97 (upper carried car), car 0.61 (lower load), truck 0.67 (rig) |
| RetinaNet | N | nothing on the carrier |
| Mask R-CNN | Y | car 0.98 (upper), car 0.74, car 0.56 (lower/rear), truck 0.65 (rig) |
| YOLO v11 | N | truck 0.86 (whole rig) |

**Fooled: 3/7** (FCOS, Faster R-CNN, Mask R-CNN).
Other notes: the many small car and truck boxes at x ≈ 680 to 930 px (DETR, FCOS, Faster, RetinaNet, Mask) are on real distant traffic, so they do not count. This is probably why the README gives 6/7. FCOS also labels the rig "motorcycle" (0.53).
**Caption:** A car transporter loaded with cars drives ahead on a two-lane highway. Three detectors report the carried cars as separate "car" objects (upper car up to 0.98, Mask R-CNN) in addition to, or instead of, the transporter. DETR, SSD and YOLO v11 report a single "truck", and RetinaNet reports nothing on the rig.

## 13. carrier_alt1 (LrDsApWs3C0): car-carrier trailer seen from the side

| Model | Error | Boxes on carried vehicles |
|---|---|---|
| DETR | Y | car 1.00 (black SUV), truck 0.89 (green Jeep), truck 0.98 and car 0.88 (white SUV), car 0.73, 0.71 (lower car) |
| SSD | Y | car 0.91, truck 0.89, truck 0.79, car 0.59 |
| FCOS | Y | car 0.85, truck 0.65, bus 0.51, truck 0.59, car 0.56, car 0.62 |
| Faster R-CNN | Y | car 0.99, truck 0.93, truck 0.75, car 0.66, car 0.67 |
| RetinaNet | Y | car 0.76, truck 0.69, truck 0.58, car 0.51 |
| Mask R-CNN | Y | car 0.99, truck 0.95, truck 0.73, car 0.66, car 0.58, car 0.57, truck 0.65 |
| YOLO v11 | Y | car 0.86, truck 0.85, car 0.79 |

**Fooled: 7/7** (all).
Other errors: DETR surfboard 0.95 on the roof of the white SUV. FCOS bus 0.51 on the Jeep. The trailer gets its own large truck box in DETR (0.99), FCOS (0.62), Faster (0.78), RetinaNet (0.58) and Mask (0.86).
**Caption:** A car-carrier trailer is loaded with an SUV, a Jeep and two other cars. All seven detectors report the carried vehicles as three to seven separate "car" or "truck" objects (up to 1.00, DETR), which a tracker could treat as independent road users. DETR also places a "surfboard" (0.95) on one vehicle's roof.

## 14. mobilityscooter_pick (1JJ3Lwcx3G0): mobility-scooter user on a cycle lane

| Model | Error | Scooter / rider |
|---|---|---|
| DETR | Y | motorcycle 0.90 / person 0.99 |
| SSD | Y | motorcycle 0.52 / rider missed |
| FCOS | Y | motorcycle 0.55 / person 0.56, 0.53 |
| Faster R-CNN | Y | motorcycle 0.96 / person 0.97; chair 0.61 on the crutches and seat |
| RetinaNet | Y | motorcycle 0.75 / person 0.69 |
| Mask R-CNN | Y | motorcycle 0.90 / person 0.97 |
| YOLO v11 | Y (missed) | scooter and rider both missed |

**Fooled: 7/7.** Six models say "motorcycle", and YOLO v11 misses both the scooter and its rider. SSD also misses the rider.
Other notes: DETR stop sign 0.98 and 0.87, FCOS 0.54, Faster 0.69 and Mask 0.53 are on round sign plates whose faces are not visible. Person boxes at the crossing are on real pedestrians.
**Caption:** An elderly person rides a four-wheeled mobility scooter along a cycle lane. Six detectors label the scooter "motorcycle", from 0.52 (SSD) to 0.96 (Faster R-CNN), and YOLO v11 detects neither the scooter nor its rider while still detecting the pedestrians farther away.

## 15. rickshaw_pick (2gTclp0JrZM): pulled rickshaw, top-down view

| Model | Error | Cart / puller |
|---|---|---|
| DETR | Y | bicycle 0.98, 0.50; suitcase 0.93 / person 1.00 |
| SSD | Y | car 0.56 / puller missed |
| FCOS | Y | suitcase 0.71, bicycle 0.52 / person 0.73 |
| Faster R-CNN | Y | motorcycle 0.68 / person 0.99 |
| RetinaNet | Y (missed) | cart missed / person 0.88 |
| Mask R-CNN | Y | suitcase 0.62 / person 1.00 |
| YOLO v11 | Y | suitcase 0.51 / puller missed |

**Fooled: 7/7.** Six give a wrong class, and RetinaNet misses the cart. YOLO v11 and SSD also miss the puller.
Other errors: DETR backpack 0.55 on the puller.
**Caption:** Seen from above, a person pulls a two-wheeled rickshaw across an intersection. The detectors force the cart into "suitcase" (up to 0.93, DETR), "bicycle" (up to 0.98), "motorcycle" (0.68) or "car" (0.56). RetinaNet ignores the cart, and YOLO v11 reports only a suitcase (0.51), without the person pulling it.

## 16. cargotrike_pick (bvYQa8ddX38): tricycle overloaded with mattresses

| Model | Error | Load / trike |
|---|---|---|
| DETR | N | no box on load / bicycle 0.96, 0.64 |
| SSD | Y | truck 0.60 / bicycle 0.87 |
| FCOS | Y | truck 0.71 / bicycle 0.55, 0.55 |
| Faster R-CNN | Y | truck 0.95 / bicycle 0.97, 0.77 |
| RetinaNet | N | no box on load / bicycle 0.62 |
| Mask R-CNN | Y | truck 0.86 / bicycle 0.93 |
| YOLO v11 | N | no box on load / bicycle 0.55 |

**Fooled: 4/7** (SSD, FCOS, Faster R-CNN, Mask R-CNN).
Other errors: Faster R-CNN tie 0.66 on the rider's open collar. The motorcycle boxes (0.57 to 0.99) are on a real parked scooter at the left, and the car boxes are on real parked cars.
**Caption:** A man pedals a cargo tricycle carrying a stack of mattresses taller than himself. Four detectors label the load "truck", from 0.60 (SSD) to 0.95 (Faster R-CNN). Every detector still labels the tricycle as a bicycle.

## 17. headload_pick (F8BCbjvjQDo): porter carrying a bale on his head

| Model | Error | Label on the head load |
|---|---|---|
| DETR | Y | handbag 0.88 |
| SSD | N | none (one person box 0.96 spans porter and load) |
| FCOS | Y | umbrella 0.55, frisbee 0.55, surfboard 0.51 |
| Faster R-CNN | Y | umbrella 0.54 |
| RetinaNet | N | none |
| Mask R-CNN | Y | umbrella 0.58 |
| YOLO v11 | Y | surfboard 0.72 |

**Fooled: 5/7** (DETR, FCOS, Faster R-CNN, Mask R-CNN, YOLO v11).
Other errors: the rolled paper in his hand becomes remote 0.57 (Faster R-CNN) and book 0.78 (Mask R-CNN). Background phantoms: Faster bottle 0.60, Mask chair 0.84, potted plant 0.69 and 0.62 (Mask), and potted plant 0.74 (DETR).
**Caption:** A porter in a busy street carries a large wrapped bale on his head. Five detectors give the bale an unrelated COCO class: "surfboard" (0.72, YOLO v11), "handbag" (0.88, DETR), "umbrella" (0.54 to 0.58) or, from FCOS, umbrella, frisbee and surfboard together. Every model detects the porter himself as "person".

## 18. horsecart_pick (CWj1cWlT558): horse team on a dirt road (small in frame)

| Model | Error | Labels on the horses |
|---|---|---|
| DETR | N | horse 0.73 to 0.99 (7 boxes) |
| SSD | N | horse 0.57 (one box for the group) |
| FCOS | N | horse 0.61, 0.53 |
| Faster R-CNN | Y | cow 0.88 (plus horse 0.61, 0.51) |
| RetinaNet | Y | cow 0.51 |
| Mask R-CNN | Y | cow 0.96 (plus horse 0.72) |
| YOLO v11 | Y | elephant 0.73 (one box for the group) |

**Fooled: 4/7** (Faster R-CNN, RetinaNet, Mask R-CNN, YOLO v11).
Other notes: the group is about 140 × 120 px. At tapestry resolution, the zoomed Original shows several horses with people on or behind them, but the cart itself is not clearly visible. No model has a class for the cart, and YOLO v11 reports no person. The person boxes from the other models are probably on the real drivers or riders.
**Caption:** A team of horses with drivers approaches on a rural dirt road. Faster R-CNN and Mask R-CNN label one horse "cow" (0.88 and 0.96), RetinaNet does likewise at 0.51, and YOLO v11 merges the whole team into a single "elephant" (0.73).

## 19. glare_pick (IAc1x02D9K0): low sun glare inside a car (WEAK)

| Model | Error | Detections |
|---|---|---|
| DETR | N | person 0.92, 0.85; car 0.53 (whole frame) |
| SSD | N | nothing |
| FCOS | N | person 0.60; car 0.53 (whole frame) |
| Faster R-CNN | N | person 0.84, 0.69 |
| RetinaNet | N | nothing |
| Mask R-CNN | N | person 0.83, 0.65, 0.54 |
| YOLO v11 | N | nothing |

**Fooled: 0/7. WEAK.** The person boxes are on the real driver at the left and a real passenger behind the right seat. They are loosely localised, but they are not phantoms. The whole-frame "car" (DETR 0.53, FCOS 0.53) is arguably correct, because the scene is a car interior. The airplane and cup in the README do not appear in this run.
**Caption:** Strong low sun floods the windscreen of a car with a driver and a passenger. No detector produces a phantom class from the glare; three detect neither occupant, and the others give coarse person boxes (0.54 to 0.92) on the real occupants.
*Recommendation:* drop this case, or keep it only as a negative example (glare causes missed occupants rather than phantoms).
