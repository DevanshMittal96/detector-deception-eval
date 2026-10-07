# Tapestry verdicts: 24 figures (run 2026-10-07)

Source: `data/figures/tapestries/` (24 tapestries and `detections.json`, threshold 0.50). Every tapestry was viewed. Each box was assigned to a real or deceptive object by comparing its `box_xyxy` (original pixels) with the Original cell, which was cropped, enlarged and overlaid with a pixel ruler where needed. All scores below come from the JSON. Model order is DETR, SSD, FCOS, Faster R-CNN (Faster), RetinaNet (Retina), Mask R-CNN (Mask), YOLO v11 (YOLO).

## Summary

| Figure | Intended error | Fooled k/7 | Which models |
|---|---|---|---|
| mannequin1 | "person" on the mannequin | **7/7** | all |
| mannequin2 | "person" on the head-form mannequin | **6/7** | DETR, FCOS, Faster, Retina, Mask, YOLO (SSD: one box merging man and mannequin) |
| mannequin3 | "person" on the market mannequin | **5/7** (7/7 counting merged boxes) | DETR, FCOS, Faster, Retina, YOLO; SSD and Mask merge it with the real person beside it |
| standee1 | "person" on the Obama cutout | **7/7** | all |
| standee2 | "person" on the Trump cutout | **7/7** | all |
| standee3 | "person" on the Reagan cutout (left figure) | **7/7** | all |
| printed_tshirt | "person" on the printed portrait | **7/7** | all (YOLO now fooled too, at 0.54) |
| printed_poster | "person" on the poster face | **5/7** | DETR, FCOS, Faster, Retina, Mask |
| printed_billboard | "person" on the billboard face | **7/7** | all |
| painting1 | "person" on painted portraits | **7/7** | all |
| painting2 | "person" on the Van Gogh self-portrait | **7/7** | all |
| painting3 | "person" on the mural barber/customer | **7/7** | all |
| mirror1 | phantom "person" on the mirror reflection | **4/7** | DETR, FCOS, Faster, Mask |
| mirror2 | phantom "person" on the mirror reflection | **3/7** | DETR, Faster, Mask |
| mirror3 | driver counted twice (direct and in mirror) | **5/7** | DETR, FCOS, Faster, Retina, Mask |
| wet | phantom object on reflections/tunnel wall | **0/7 WEAK** | none |
| fog1 | missed vehicles/pedestrian | **2/7** | SSD, YOLO |
| fog2 | missed car in dense fog / phantom labels | **7/7** | all (6 empty; DETR only phantoms) |
| fog3 | missed distant cars | **3/7** (5/7 counting a single faint miss) | SSD, YOLO, Retina (DETR and Mask miss only the faintest car) |
| rain1 | missed vehicles / phantom labels | **7/7** | all miss the vehicles; DETR, FCOS, Faster add phantom labels |
| rain2 | missed scooter rider / phantoms | **5/7** | FCOS, Faster, Retina, Mask, YOLO miss the rider |
| rain3 | no car ahead separated | **7/7** | all |
| rain4 | missed cars / phantom mirror person | **5/7** | DETR, SSD, Faster, Mask, YOLO |
| blur | missed car ahead / phantom label | **5/7** | DETR, SSD, FCOS, Retina, YOLO |

Only **wet** is WEAK (fewer than 2 models fooled). fog1 is borderline at exactly 2/7.

Changes from the earlier, higher-resolution run (README "Chosen images"): printed_tshirt went from 6/7 to 7/7, painting2 from 4/7 to 7/7, and printed_poster from 6/7 to 5/7 (SSD now boxes only the man). wet went from 2/7 to 0/7 because the phantom "train" is gone. mirror1 no longer shows a DETR "cow", rain1 no longer shows a Mask R-CNN "knife", and in rain4 YOLO now misses 1 of 3 cars, not 3 of 4.

---

## mannequin1 (unsplash-KnZ73fNXERM)
Scene: a white faceless mannequin on a plinth (x≈540–990, y≈700–2010) with a real woman just behind it (x≈780–1020), and small distant pedestrians and parked vehicles.
- DETR: **Y** person 0.98 [554,714,999,2014]; the woman gets 0.95
- SSD: **Y** person 1.00; the woman gets 0.90
- FCOS: **Y** person 0.83; the woman gets 0.55
- Faster: **Y** person 1.00; the woman gets 0.97
- Retina: **Y** person 0.96 [543,684,1014,2009]. This single box follows the mannequin from head to plinth, and the woman gets no box of her own
- Mask: **Y** person 1.00; the woman gets 0.98
- YOLO: **Y** person 0.89; the woman gets 0.75

**Fooled: 7/7** (all models).
Other errors: the parked vehicle on the right gets both car and truck labels (DETR, FCOS, Retina). RetinaNet misses the real woman as a separate instance. The distant pedestrians are real people and are not counted.
Caption: *A faceless display mannequin standing beside a woman is labelled "person" by all seven detectors, with scores from 0.83 (FCOS) to 1.00 (SSD, Faster R-CNN, Mask R-CNN). RetinaNet places a single box (0.96) on the mannequin and gives the real woman no separate detection.*

## mannequin2 (pexels-6050412)
Scene: an elderly man (x≈1450–3450) adjusts a suit on a mannequin that has a blank cloth head under a flat cap (x≈2700–4530). Clothes hang on the left.
- DETR: **Y** person 1.00 [2820,246,4532,3778]; tie 1.00 on the mannequin
- SSD: **N**. Its one box, person 0.94 [1783,256,3904,3833], straddles the man and the mannequin and cannot be assigned to either
- FCOS: **Y** person 0.82 [2728,247,4533,3734]
- Faster: **Y** person 0.99 [2723,297,4500,3800]
- Retina: **Y** person 0.89 [2715,261,4583,3778]
- Mask: **Y** person 0.99 [2642,369,4509,3776]
- YOLO: **Y** person 0.87 [2669,263,4501,3796]

**Fooled: 6/7** (DETR, FCOS, Faster, Retina, Mask, YOLO).
Other errors: phantom "person" boxes on the clothes hanging at the left (DETR 0.95 and 0.67, FCOS 0.53, Faster 0.86, Mask 0.79 and 0.78). There are also furniture labels on the display at the right edge (Faster: dining table 0.80, vase 0.73; Mask: refrigerator 0.84, dining table 0.67). Every model except SSD reports a "tie" on the mannequin (0.66–1.00).
Caption: *A tailor's mannequin with a blank cloth head is detected as "person" by six of seven models (0.82–1.00), and four of them also label the clothes hanging on the left as "person" (0.53–0.95). SSD returns a single person box (0.94) spanning both the real man and the mannequin.*

## mannequin3 (unsplash-GY72UnGa58s)
Scene: a dark-blue male mannequin in a checked shirt in the right foreground (x≈560–1070, y≈390–800). Beside it is a real person in a rainbow wig (x≈420–790), a bearded man (x≈260–440), and a crowded market behind.
- DETR: **Y** person 0.52 [560,400,1072,798]. Its 0.99 box [423,391,1072,798] merges the wig-wearer with the mannequin
- SSD: **ambiguous**. Person 0.92 [429,358,1052,806] covers the wig-wearer and the mannequin together
- FCOS: **Y** person 0.66 [448,340,1060,798]; the wig-wearer has a separate box (0.51)
- Faster: **Y** person 0.83 [751,415,1064,794] (plus 0.99 [465,377,998,802] across both)
- Retina: **Y** person 0.88 [509,413,1074,806]; the wig-wearer has a separate box (0.63)
- Mask: **ambiguous**. Person 1.00 [444,378,980,796] covers both, with no separate box for the wig-wearer
- YOLO: **Y** person 0.74 [559,389,1068,805]

**Fooled: 5/7 strict** (DETR, FCOS, Faster, Retina, YOLO). It is 7/7 if the merged SSD and Mask boxes are counted.
Other errors: Faster reports "umbrella" 0.66 on the awning at the top and several backpack/handbag boxes. Mask labels the clothing at the lower left "suitcase" (0.90). The figure in a beige jacket at the left (x≈115–215) may be a second, headless mannequin, and most models box it as "person" (for example Faster 0.92, Mask 0.96). This was not counted.
Caption: *In a crowded market, five of seven detectors place a dedicated "person" box on a dark-blue display mannequin (0.52–0.88). SSD (0.92) and Mask R-CNN (1.00) merge the mannequin and the adjacent shopper into a single "person" detection.*

## standee1 (commons-3013397193)
Scene: a life-size Obama cardboard cutout (x≈350–525) between two real women.
- DETR: **Y** person 1.00 [352,67,524,602]
- SSD: **Y** person 0.84 [336,82,494,611]
- FCOS: **Y** person 0.75 [347,72,518,578]
- Faster: **Y** person 1.00 [350,66,523,601]
- Retina: **Y** person 0.91 [346,65,528,602]
- Mask: **Y** person 1.00 [355,64,524,590]
- YOLO: **Y** person 0.88 [351,69,521,605]

**Fooled: 7/7.**
Other errors: there is a "tie" on the printed tie (DETR 0.99, Faster 0.99, Mask 0.99, YOLO 0.71, FCOS 0.62), and DETR labels the cutout's hands "cell phone" 0.96. Faster (0.72, 0.56) and Mask (0.69) report a "teddy bear" in the pumpkin and gourd display, and Mask labels the bed a "couch" 0.59. The Obama–Biden sign is labelled "book" (0.58–0.95) by five models.
Caption: *A cardboard cutout standing between two women is detected as "person" by all seven models, with scores from 0.75 (FCOS) to 1.00 (DETR, Faster R-CNN, Mask R-CNN). Several detectors also report a "tie" on the printed suit and a "teddy bear" in the decorative gourds.*

## standee2 (commons-48555421596)
Scene: a Trump cardboard cutout (x≈180–440) at the road edge next to a reporter in red (x≈490–750), with a crowd behind.
- DETR: **Y** person 1.00 [176,61,561,926]
- SSD: **Y** person 1.00 [177,59,484,928]
- FCOS: **Y** person 0.80 [174,62,448,944]
- Faster: **Y** person 1.00 [189,63,434,936]
- Retina: **Y** person 0.87 [167,67,500,922]
- Mask: **Y** person 1.00 [177,79,485,925]
- YOLO: **Y** person 0.84 [176,63,552,931]

**Fooled: 7/7.**
Other errors: there is a "tie" on the cutout (DETR 1.00, Faster 1.00, Mask 1.00, YOLO 0.69, FCOS 0.51). Faster labels the microphone "baseball bat" 0.53, and DETR and Mask add small handbag/cell-phone/umbrella boxes in the crowd. A photographer watermark is visible at the bottom left.
Caption: *A roadside cardboard cutout is detected as "person" by all seven models, six of them with scores of 0.84–1.00, in boxes comparable to the one given to the real reporter beside it. Five models also detect a "tie" on the printed suit.*

## standee3 (commons-Reagan_cutout)
Scene: the left figure (x≈30–230) is the cutout; the real Reagan on the right (x≈205–420) has his arm around its shoulder.
- DETR: **Y** person 1.00 [39,27,228,466]
- SSD: **Y** person 1.00 [37,30,232,463]
- FCOS: **Y** person 0.87 [40,32,227,461]
- Faster: **Y** person 1.00 [31,30,231,462]
- Retina: **Y** person 0.97 [40,38,227,460]
- Mask: **Y** person 1.00 [28,33,229,464]
- YOLO: **Y** person 0.91 [43,24,229,466]

**Fooled: 7/7.**
Other errors: there is a "tie" on the cutout (0.71–1.00, every model except SSD). Bottles on the buffet table are detected correctly. Apart from the cutout, there are no phantom classes.
Caption: *A cardboard cutout of Ronald Reagan (left) receives a "person" detection from every model (0.87–1.00), with scores equal to or above those given to Reagan himself (0.86–1.00). No detector distinguishes the printed figure from the real one.*

## printed_tshirt (unsplash-DDP6J9nHU1o)
Scene: a man in a hat seen from behind, with a portrait of a woman printed on the back of his T-shirt (x≈240–600, y≈640–950). Bystanders are at the edges.
- DETR: **Y** person 0.93 [238,653,636,1022] (also 0.64 [246,651,587,942])
- SSD: **Y** person 0.87 [231,644,567,956]
- FCOS: **Y** person 0.74 [246,642,591,940]
- Faster: **Y** person 0.96 [241,643,591,945]
- Retina: **Y** person 0.79 [235,647,604,941]
- Mask: **Y** person 0.97 [133,650,610,992]
- YOLO: **Y** person 0.54 [244,648,580,936]

**Fooled: 7/7.** In the earlier run YOLO was not fooled.
Other errors: DETR and Mask produce several redundant overlapping "person" boxes on the wearer and the print (Mask has 8 person boxes). The edge bystanders are real people.
Caption: *A portrait printed on the back of a T-shirt is detected as a separate "person" by all seven models, from 0.54 (YOLO v11) to 0.97 (Mask R-CNN), in addition to the wearer himself.*

## printed_poster (unsplash-V2X6NTBJdxU)
Scene: a man with headphones (x≈165–600) walks past a large poster of a reclining face that fills most of the frame (x≈170–1110).
- DETR: **Y** person 0.71 [174,92,1075,773] (plus tv 0.55 on the poster)
- SSD: **N**. Only the man is detected (0.99)
- FCOS: **Y** person 0.56 [169,55,1112,757]
- Faster: **Y** person 0.86 [236,95,1001,770]
- Retina: **Y** person 0.64 [183,93,1028,765]
- Mask: **Y** person 0.78 [347,80,1028,778]
- YOLO: **N**. Only the man is detected (0.91)

**Fooled: 5/7** (DETR, FCOS, Faster, Retina, Mask).
Other errors: DETR labels the poster "tv" 0.55. Faster labels the left border "book" 0.50. DETR (0.73) and Faster (0.62) put small "person" boxes on the dark strip at the right edge (x≈1120–1156), which could not be verified at this resolution. A real backpack or bag is detected correctly by DETR and FCOS.
Caption: *A large poster of a face behind a passing pedestrian is detected as an additional "person" by five of seven models (0.56–0.86). SSD and YOLO v11 detect only the real pedestrian.*

## printed_billboard (unsplash-XX99bsQcfwY)
Scene: a motion-blurred woman (x≈230–550) walks past a billboard of a woman's face and shoulders (x≈470–1170).
- DETR: **Y** person 1.00 [534,68,1169,721]
- SSD: **Y** person 0.96 [521,75,1171,730]
- FCOS: **Y** person 0.73 [488,65,1171,719]
- Faster: **Y** person 1.00 [468,61,1161,718]
- Retina: **Y** person 0.95 [526,52,1171,720]
- Mask: **Y** person 1.00 [511,47,1153,725]
- YOLO: **Y** person 0.85 [523,66,1170,714]

**Fooled: 7/7.**
Other errors: the billboard model's earring is labelled "cell phone" (DETR 0.99, FCOS 0.60, Mask 0.60). The bollard at the right is labelled "bottle" 0.72 and "chair" 0.68 (Faster) and "chair" 0.66 (Mask).
Caption: *A billboard portrait is detected as "person" by all seven models (0.73–1.00), in five of seven cases with a score at least as high as that of the real, motion-blurred pedestrian in front of it. Three models also label the model's earring "cell phone".*

## painting1 (pexels-11770961)
Scene: an elderly painter seen from behind (x≈520–2240) works on a portrait on the easel (x≈1940–2650, y≈1170–2550). The studio walls hold many framed portraits.
- DETR: **Y** person 0.98 [1780,1190,2658,3277] on the easel portrait, and also 1.00 on a framed portrait [1935,757,2220,1325]
- SSD: **Y** person 0.81 [1937,1177,2632,2562]
- FCOS: **Y** person 0.66 [1924,1173,2666,2524]
- Faster: **Y** person 0.95 [1901,1151,2669,2457], and 0.98 on a framed portrait
- Retina: **Y** person 0.71 [1954,1164,2728,2500]
- Mask: **Y** person 0.97 [1912,1183,2675,2415], and 0.97 on a framed portrait
- YOLO: **Y** person 0.62 [1989,1188,2659,2470], and 0.59 on the small portrait at the left [228,1123,591,1548]

**Fooled: 7/7.**
Other errors: DETR, FCOS, Faster, Retina and Mask report a "tie" on the painted portraits (0.51–0.97). There are also "bottle" boxes (Faster 0.55; Mask 0.78, 0.66), "book" (Faster 0.70, Mask 0.62) and "tv" (Mask 0.64) on paintings and frames. DETR, FCOS, Faster and Mask produce up to 10 extra "person" boxes on wall portraits.
Caption: *The portrait on the painter's easel is detected as "person" by all seven models (0.62–0.98), and DETR, FCOS, Faster R-CNN and Mask R-CNN add further "person" boxes on framed portraits around the studio. Five models also assign a "tie" to at least one painted figure.*

## painting2 (unsplash-f5MWSw11jjo)
Scene: Van Gogh's self-portrait (figure at x≈470–690, y≈240–520) is seen between three silhouetted visitors, one of them photographing it with a phone.
- DETR: **Y** person 0.98 [469,247,690,514]
- SSD: **Y** person 0.86 [481,288,668,513]
- FCOS: **Y** person 0.78 [475,242,690,516]
- Faster: **Y** person 0.94 [482,272,679,517]
- Retina: **Y** person 0.68 [473,251,683,517]
- Mask: **Y** person 0.96 [480,256,675,503]
- YOLO: **Y** person 0.61 [469,246,687,517]

**Fooled: 7/7.** In the earlier run it was 4/7, with Mask also reporting a "dog"; there is no "dog" in this run.
Other errors: none. The phone is correctly labelled "cell phone" (0.59–0.98) and the visitors are real.
Caption: *Van Gogh's painted self-portrait is detected as "person" by all seven models (0.61–0.98), alongside the museum visitors in the foreground. DETR assigns the painting (0.98) nearly the same score as the closest visitor (0.99).*

## painting3 (unsplash-6NWW4AZGKtg)
Scene: a barbershop mural with a painted barber (x≈630–745), a seated customer (x≈680–860), a woman at the right and a man at the left. A real scooter rider (x≈230–585) passes in front and a real pedestrian (x≈995–1080) walks at the right.
- DETR: **Y** person 0.99 [630,326,744,620] (barber), and 0.58 on the painted man at the left
- SSD: **Y** person 0.66 [629,326,720,639]
- FCOS: **Y** person 0.79 [631,326,717,622]
- Faster: **Y** person 0.99 (barber) and 0.97 [681,358,858,613] (customer), and 0.63 on the painted woman
- Retina: **Y** person 0.67 (barber) and 0.66 (customer)
- Mask: **Y** person 0.98 (barber) and 0.86 (customer)
- YOLO: **Y** person 0.77 (barber), and 0.57 on the painted man at the left

**Fooled: 7/7.**
Other errors: DETR reports "dog" 0.77 on the painted customer's head and "suitcase" 0.93 on the scooter's top box, and labels the area around the parked scooter "person" (0.72, 0.70). SSD labels the shopping trolley "skateboard" 0.79. Mask labels the street lamp "traffic light" 0.63. YOLO labels the parked bicycles "motorcycle" 0.52, and FCOS labels the scooter box "suitcase" 0.51.
Caption: *The painted barber in a street mural is detected as "person" by all seven models (0.66–0.99), and five models also detect the painted customer or other mural figures. Several models add unrelated phantom classes, including "dog" (DETR, 0.77) on the painted customer's head and "skateboard" (SSD, 0.79) on a shopping trolley.*

## mirror1 (unsplash-uIOEJbcEVh8)
Scene: the view through a windshield. The only human is a man's face reflected in the rear-view mirror (x≈490–940, y≈245–475).
- DETR: **Y** person 0.94 [497,327,734,463] (also 0.52)
- SSD: **N**
- FCOS: **Y** person 0.51 [500,243,932,474]
- Faster: **Y** person 0.65 [490,313,937,467] (also 0.60)
- Retina: **N**
- Mask: **Y** person 0.75 [486,320,940,474] (also 0.53)
- YOLO: **N** (no detections)

**Fooled: 4/7** (DETR, FCOS, Faster, Mask).
Other errors: there is a whole-frame "car" box from six models (0.61–0.93), which is the car interior seen from inside. Faster (0.77) and Mask (0.68) label the dashboard corner "chair", and Mask reports "dog" 0.54 over the desert scrub. The DETR "cow" from the earlier run is absent.
Caption: *A face visible only as a reflection in the rear-view mirror is detected as "person" by four of seven models (DETR 0.94, Mask R-CNN 0.75, Faster R-CNN 0.65, FCOS 0.51). Mask R-CNN additionally reports a "dog" (0.54) in the roadside scrub.*

## mirror2 (unsplash-e8f21--1XT8)
Scene: a woman's face reflected in the rear-view mirror (x≈600–1000, y≈120–345), with a blurred road beyond.
- DETR: **Y** person 0.88 [604,21,999,337] (also 0.73)
- SSD: **N** (no detections)
- FCOS: **N** (labels the mirror "car" 0.57)
- Faster: **Y** person 0.84 [598,130,1000,345]
- Retina: **N**
- Mask: **Y** person 0.83 [599,122,1009,347] (also 0.60)
- YOLO: **N** (no detections)

**Fooled: 3/7** (DETR, Faster, Mask).
Other errors: the mirror itself is labelled "car" (FCOS 0.57) and "tv" (Faster 0.50). DETR (0.74) and RetinaNet (0.56) give the frame a large "car" box.
Caption: *The reflection of a driver in the rear-view mirror is detected as "person" by DETR (0.88), Faster R-CNN (0.84) and Mask R-CNN (0.83). FCOS and Faster R-CNN label the mirror housing "car" (0.57) and "tv" (0.50) respectively.*

## mirror3 (unsplash-Y0FE0azIgc8)
Scene: a woman driving (x≈0–700), with her face also visible in the rear-view mirror (x≈760–995, y≈80–195).
- DETR: **Y** person 0.99 [785,88,986,186]; driver 1.00
- SSD: **N**. Driver only (0.96)
- FCOS: **Y** person 0.65 [774,86,973,188]; driver 0.77
- Faster: **Y** person 0.93 [758,77,985,192]; driver 1.00
- Retina: **Y** person 0.61 [776,86,983,185]; driver 0.92
- Mask: **Y** person 0.95 [761,42,995,197]; driver 1.00
- YOLO: **N**. Driver only (0.88)

**Fooled: 5/7** (DETR, FCOS, Faster, Retina, Mask).
Other errors: DETR labels the infotainment screen "cell phone" 0.97 and puts a second "cell phone" 0.52 near the steering wheel. Faster (0.54) and Mask (0.58) call the screen "tv". Mask adds a duplicate "person" 0.71 on the driver's lower body. Five models give the cabin a large "car" box.
Caption: *The driver is counted twice by five of seven models: once directly (0.77–1.00) and once as her reflection in the rear-view mirror (0.61–0.99). Only SSD and YOLO v11 report a single person.*

## wet (unsplash-rcOQvvVFQ-g) **WEAK**
Scene: a car in a narrow green-lit tunnel at night, with red taillight reflections on the wet floor and the brick wall.
- DETR **N** (car 1.00), SSD **N** (car 0.91), FCOS **N** (car 0.87), Faster **N** (car 0.99), Retina **N** (car 0.89), Mask **N** (car 0.99), YOLO **N** (car 0.85)

**Fooled: 0/7. WEAK.**
Other errors: none. Each model returns exactly one correct "car" box. The phantom "train" on the wall (Faster 0.61, Mask 0.57) from the earlier run does not reproduce. The input appears to be a low-resolution copy (about 440 px wide), which may explain this. Consider re-running on the full-resolution file or dropping the figure.
Caption (if kept): *Despite strong red reflections on the wet floor and tunnel wall, all seven models return a single correct "car" detection (0.85–1.00) and no phantom objects.*

## fog1 (unsplash-8HFYuC3t00E)
Scene: a lone pedestrian (x≈575–615) crossing a foggy street. Two vehicles are at the left (near x≈10–118, far x≈170–233) and a traffic light is lit.
- DETR **N**: finds all
- SSD **Y**: no detections at all; misses the pedestrian, both vehicles and the traffic light
- FCOS **N**: finds all
- Faster **N**: finds all
- Retina **N**: finds all
- Mask **N**: finds all
- YOLO **Y**: misses both vehicles; finds the pedestrian 0.77 and the traffic light 0.60

**Fooled: 2/7** (SSD, YOLO). This is borderline.
Other errors: DETR (truck 0.98 and car 0.70), FCOS and Mask give the near-left vehicle both "car" and "truck" boxes.
Caption: *In heavy fog, SSD returns no detections and YOLO v11 misses both vehicles, while finding the pedestrian (0.77). The remaining five models detect the pedestrian (0.79–1.00) and both vehicles.*

## fog2 (pexels-30546867)
Scene: a single car is visible only as two headlights in dense night fog, beside a guard rail.
- DETR **Y**: misses the car, reports "airplane" 0.78 [276,814,1325,2510] and "fork" 0.55 [291,808,580,977] on the guard rail
- SSD, FCOS, Faster, Retina, Mask, YOLO **Y**: no detections

**Fooled: 7/7.**
Caption: *No model detects the oncoming car whose headlights are visible through dense fog. Six models return nothing, and DETR reports phantom "airplane" (0.78) and "fork" (0.55) boxes over the road and guard rail.*

## fog3 (unsplash-K8G3irhZpWs)
Scene: two near cars (x≈680–780 and 888–1005) and three distant vehicles fading into fog (at about x 538–587, 585–618 and 514–546).
- DETR **N (minor)**: finds 4 of 5 and misses the faintest at x≈514. The vehicle at x≈585 gets both "truck" 0.94 and "car" 0.75
- SSD **Y**: 2 of 5 (0.83, 0.69)
- FCOS **N**: 5 of 5 (0.60–0.89)
- Faster **N**: 5 of 5 (0.59–1.00, one duplicate)
- Retina **Y**: 3 of 5 (0.84–0.97)
- Mask **N (minor)**: 4 of 5, missing the faintest
- YOLO **Y**: 2 of 5 (0.84, 0.82)

**Fooled: 3/7** (SSD, YOLO, Retina miss two or more). It is 5/7 if missing only the faintest vehicle counts.
Caption: *As vehicles fade into fog, SSD and YOLO v11 detect only the two nearest cars and RetinaNet three, whereas FCOS and Faster R-CNN recover all five (down to 0.59).*

## rain1 (unsplash-YZ7O7Okhd2o)
Scene: a rain-covered windshield at night. Traffic ahead is visible only as blurred tail-lights and street lights; a dark occupant silhouette is at the lower right.
- DETR **Y**: no vehicle; phantom "airplane" 0.96 over the windshield
- SSD **Y**: no detections
- FCOS **Y**: no vehicle; phantom "umbrella" 0.55
- Faster **Y**: no vehicle; phantom "clock" 0.54. The "person" 0.92 at the lower right lies on the occupant silhouette and is probably genuine
- Retina **Y**: no detections
- Mask **Y**: no vehicle. Its "person" 0.80 is on the same silhouette
- YOLO **Y**: no detections

**Fooled: 7/7** on missed vehicles; 3/7 also add phantom classes.
Note: the earlier run's Mask "knife" is absent.
Caption: *Through a rain-covered windshield at night, no model detects the vehicles ahead. SSD, RetinaNet and YOLO v11 return nothing, and DETR, FCOS and Faster R-CNN report phantom "airplane" (0.96), "umbrella" (0.55) and "clock" (0.54) boxes.*

## rain2 (unsplash-CnVGO6fae38)
Scene: the driver's view in a dark cab, with the real driver at the left (x≈230–650). A scooter rider in a red raincoat is ahead through the wet windshield (about x 600–700, y 340–480).
- DETR **N**: rider 0.97 [611,343,703,469]
- SSD **N**: rider 0.84 [604,336,704,484]
- FCOS **Y**: misses the rider
- Faster **Y**: misses the rider
- Retina **Y**: misses the rider
- Mask **Y**: misses the rider
- YOLO **Y**: no detections at all; misses the driver too

**Fooled: 5/7** (FCOS, Faster, Retina, Mask, YOLO).
Other errors: the driver's arm and hand on the wheel are labelled "cow" (DETR 0.88, Faster 0.78, Retina 0.54), "dog" (FCOS 0.52) and "backpack" (Mask 0.62).
Caption: *Only DETR (0.97) and SSD (0.84) detect the scooter rider ahead through the rain-streaked windshield, and YOLO v11 returns no detections at all. Four models label the driver's arm as an animal or object, including "cow" (DETR 0.88, Faster R-CNN 0.78).*

## rain3 (pexels-1600909)
Scene: a heavily speckled windshield. Faint car tail-lights are ahead, and the dashboard is in the foreground.
- DETR **Y**: one large "car" 0.99 over the dashboard and lower frame; nothing ahead
- SSD **Y**: whole-frame "car" 0.83
- FCOS **Y**: whole-frame "car" 0.63
- Faster **Y**: lower-frame "car" 0.87
- Retina **Y**: no detections
- Mask **Y**: three overlapping frame-sized "car" boxes (0.89, 0.54, 0.52)
- YOLO **Y**: no detections

**Fooled: 7/7.** No model localises any vehicle ahead.
Other errors: the speedometer is labelled "clock" (DETR 0.85, FCOS 0.69).
Caption: *Through a rain-speckled windshield, no model localises the vehicles ahead. Five produce only frame-sized "car" boxes that cover the vehicle's own dashboard, and RetinaNet and YOLO v11 return nothing.*

## rain4 (commons-5124407306)
Scene: a driver in heavy rain. Three cars are ahead (a pickup at x≈262–384, an SUV at x≈447–523 and a car at x≈645–744), with tiny distant vehicles. The driver's face appears in the rear-view mirror (x≈590–770, y≈125–207).
- DETR **Y**: all 3 cars, but a phantom mirror "person" 0.94 [613,132,762,202]
- SSD **Y**: misses 2 of 3 cars (finds the pickup only, 0.52)
- FCOS **N**: 3 of 3 cars (0.53–0.69), no mirror person
- Faster **Y**: 3 of 3 cars, but a mirror "person" 0.82 and "mouse" 0.87 on the dashboard/steering column
- Retina **N**: 3 of 3 cars (0.50–0.73)
- Mask **Y**: 3 of 3 cars, but a mirror "person" 0.87 and "mouse" 0.64
- YOLO **Y**: misses the right-hand car (finds 0.52 and 0.70)

**Fooled: 5/7** (DETR, SSD, Faster, Mask, YOLO).
Other errors: there are cabin-sized "car" boxes from all models. Mask labels the pickup both "car" 0.84 and "truck" 0.55.
Caption: *In heavy rain, SSD detects only one of three cars ahead and YOLO v11 two, while DETR, Faster R-CNN and Mask R-CNN detect all three but also report a phantom "person" in the rear-view mirror (0.82–0.94). Faster R-CNN and Mask R-CNN additionally label part of the dashboard "mouse" (0.87, 0.64).*

## blur (unsplash-LoTCbqVwR-0)
Scene: a motion-blurred tunnel with a car ahead (x≈422–560, y≈660–728) and a smaller vehicle to its right (x≈539–575).
- DETR **Y**: misses both; whole-frame "train" 0.65
- SSD **Y**: no detections
- FCOS **Y**: misses the main car; small vehicle only (0.65)
- Faster **N**: main car 0.95, small vehicle 0.96 (plus 0.76 duplicate)
- Retina **Y**: no detections
- Mask **N**: main car 0.74, small vehicle 0.96
- YOLO **Y**: no detections

**Fooled: 5/7** (DETR, SSD, FCOS, Retina, YOLO).
Caption: *Under strong motion blur, only Faster R-CNN (0.95) and Mask R-CNN (0.74) detect the car directly ahead. SSD, RetinaNet and YOLO v11 return nothing, FCOS finds only a smaller vehicle beside it, and DETR labels the entire frame "train" (0.65).*
