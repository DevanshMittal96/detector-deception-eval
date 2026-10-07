# Tapestry verdicts: alternates (run 2026-10-07)

Source: `data/alternates/tapestries/` (22 tapestries + `detections.json`, threshold 0.50).
Grid: Original, DETR, SSD, FCOS / Faster R-CNN, RetinaNet, Mask R-CNN, YOLO v11.
Every tapestry was viewed; all scores below come from `detections.json` (rounded to 2 d.p.).

**Counting rule.** "Fooled" means the model makes the intended error:
- Non-human figure (mannequin, standee, poster, painting): "person" on that figure.
- Mirror or reflection: any detection placed on the reflected content.
- Fog, rain or blur: a missed main road user, or a road user that gets only a wrong label, or a phantom road-user label.

Extra wrong-class boxes on an object that also gets the correct label are listed as "other errors", not counted.

## Summary

| # | Tapestry | README name | Fooled | Models fooled | Strong (>=5/7) | Differs from README? |
|---|---|---|---|---|---|---|
| 1 | wet_alt1 | wet_x1 | **3/7** | FCOS, Faster R-CNN, Mask R-CNN | no | yes (README 2/7; FCOS also fires on the puddle) |
| 2 | wet_alt2 | wet_x2 | **5/7** | DETR, FCOS, Faster R-CNN, Mask R-CNN, YOLO | **yes** | adds the full count (README listed only train / parking meter) |
| 3 | wet_alt3 | wet_x3 | **7/7** | all | **yes** (see caveat) | no |
| 4 | mirror1_alt1 | mirror_b_child_side | **7/7** | all | **yes** | no |
| 5 | mirror1_alt2 | mirror_b_sidemasks | **7/7** | all | **yes** | no |
| 6 | mirror3_alt1 | mirror3_b_teen | **6/7** | all except YOLO | **yes** | yes (README 7/7; YOLO returns nothing) |
| 7 | standee1_alt1 | standee_people_pose | **7/7** (Michelle cutout); 6/7 (Barack cutout, YOLO misses) | all | **yes** | partly |
| 8 | standee1_alt2 | standee_superman | **7/7** | all | **yes** | no |
| 9 | standee1_alt3 | standee_obama_ottawa1 | **7/7** | all | **yes** | no |
| 10 | mannequin1_alt1 | mannequin_b_lying | **0/7** "person"; 2/7 "airplane" | (Faster R-CNN, Mask R-CNN: airplane) | no | yes on scores (Mask airplane is 0.84, not 0.93–0.95) |
| 11 | mannequin1_alt2 | mannequin_b_pole | **7/7** | all | **yes** | no |
| 12 | mannequin1_alt3 | mannequin1 (Thirdman) | **1/7** | RetinaNet | no | no (weak) |
| 13 | mannequin2_alt1 | mannequin2 (Baranov) | **3/7** | DETR, Faster R-CNN, Mask R-CNN | no | no (weak) |
| 14 | painting3_alt1 | painting3_b1 | **0/7** on the main mural; 3/7 on a small painted figure | (DETR, Faster R-CNN, Mask R-CNN) | no | no |
| 15 | printed_poster_alt1 | printed_poster | **3/7** | SSD, Faster R-CNN, Mask R-CNN | no | no |
| 16 | blur_alt1 | blur | **2/7** | SSD, YOLO | no | no |
| 17 | rain4_alt1 | rain4_b_pickup | **2/7** | SSD, YOLO | no | yes (README says only SSD misses) |
| 18 | fog1_alt1 | fog1 (Podzolkin) | **2/7** | SSD, YOLO | no | no |
| 19 | fog1_alt2 | fog1_b_pexcyclist | **2/7** | SSD, YOLO (bicycle missed) | no | no |
| 20 | fog1_alt3 | fog_b_bridge_night | **3/7** | DETR, Faster R-CNN (phantom person), SSD (missed pedestrian) | no | no |
| 21 | fog2_alt1 | fog2_b_moto3 | **2/7** | SSD, YOLO | no | no |
| 22 | fog2_alt2 | fog2 (Bringas) | **3/7** | SSD (missed motorcycle), Faster R-CNN, Mask R-CNN (phantom car on dashboard) | no | no |

**Strong alternates (>=5/7):** wet_alt2, wet_alt3, mirror1_alt1, mirror1_alt2, mirror3_alt1, standee1_alt1, standee1_alt2, standee1_alt3, mannequin1_alt2 (9 of 22).
No fog, rain, blur, painting or poster alternate reaches 5/7.

### Wet recommendation (priority)

**Use wet_alt2 (wet_x2) for the "wet" figure.** It is the only alternate whose reflection is on a genuinely wet road surface: an inverted person and truck in a puddle. Five of seven models put a box on the reflection:
- DETR: suitcase 0.71, train 0.62, car 0.58
- FCOS: parking meter 0.56
- Faster R-CNN: person 0.74, train 0.65, parking meter 0.55
- Mask R-CNN: train 0.69/0.53, person 0.67
- YOLO: parking meter 0.71

SSD (no detections at all) and RetinaNet (real legs only) are not fooled. Limitations:
- The labels are mixed and the scores moderate (0.53–0.74).
- The reflection fills most of the frame, so readers will not see a conventional road scene.
- The Faster R-CNN "person 0.74" box (y 15–847) spans the real legs as well as the reflection.

**wet_alt3 (wet_x3)** scores 7/7, but it is a shop-window (glass) reflection, not a wet surface. From the image alone it is also not fully certain that the pedestrian is a reflection rather than a person seen through the glass: he is semi-transparent and mirrored text is visible on the reflected vehicle, which supports a reflection. It fits a general "reflections" figure, or a mirror figure, better than a "wet road" figure. If the caption calls the pedestrian a reflection, that claim should be checked at full resolution.

**wet_alt1 (wet_x1)** is weak: 3/7, with scores of 0.50–0.78 on the puddle and no detections on the puddle from DETR, SSD, RetinaNet or YOLO.

---

## Per-image verdicts

### 1. wet_alt1 (wet_x1): people reflected in a crosswalk puddle
**Fooled: 3/7.** FCOS (person 0.54, backpack 0.50 on the puddle), Faster R-CNN (person 0.55, 0.55, 0.51 on the puddle), Mask R-CNN (person 0.78 and 0.68 on the puddle). Not fooled: DETR, SSD, RetinaNet, YOLO.

Other errors, all on the real scene:
- "suitcase" on a pedestrian's bag or legs: DETR 0.95, Faster R-CNN 0.68, Mask R-CNN 0.51.
- "skateboard": Faster R-CNN 0.55, Mask R-CNN 0.51.

The real pedestrians and the traffic light are detected by all seven models.

*Caption:* Pedestrians on a crosswalk are mirrored in a large puddle in the foreground. All seven detectors find the real pedestrians. Three of them also report persons in the reflection: Mask R-CNN (0.78, 0.68), Faster R-CNN (0.55, 0.55, 0.51) and FCOS (0.54, plus a backpack at 0.50).

### 2. wet_alt2 (wet_x2): person and truck reflected in a puddle
**Fooled: 5/7.** All of the following boxes are on the inverted reflection:
- DETR: suitcase 0.71, train 0.62, car 0.58
- FCOS: parking meter 0.56
- Faster R-CNN: person 0.74 (box also takes in the real legs), train 0.65, parking meter 0.55
- Mask R-CNN: train 0.69, person 0.67, train 0.53
- YOLO: parking meter 0.71

Not fooled: SSD (no detections) and RetinaNet (real legs only, person 0.62/0.51).

Other notes:
- The real person and truck at the top edge are found as person by DETR, Faster R-CNN, RetinaNet, Mask R-CNN and YOLO.
- The real truck is labelled truck by DETR (0.71) and car by FCOS, Faster R-CNN and Mask R-CNN (0.50–0.86).
- SSD misses the real objects as well.

*Caption:* A person and a truck are reflected upside-down in a roadside puddle; only their wheels and feet appear directly at the top of the frame. Five of seven detectors place boxes on the reflection, with labels including "train" (Mask R-CNN 0.69, Faster R-CNN 0.65, DETR 0.62), "parking meter" (YOLO 0.71, FCOS 0.56, Faster R-CNN 0.55), "suitcase" (DETR 0.71) and "person" (Faster R-CNN 0.74, Mask R-CNN 0.67). SSD and RetinaNet report nothing on the reflection.

### 3. wet_alt3 (wet_x3): shop-window reflection of a street and a pedestrian
**Fooled: 7/7.** All seven report "person" on the semi-transparent pedestrian in the glass: DETR 1.00, Faster R-CNN 0.99, Mask R-CNN 0.99, SSD 0.96, YOLO 0.89, RetinaNet 0.86, FCOS 0.76.

Other notes:
- Reflected vehicles (pickup, bus) are labelled car by six models; SSD is the exception.
  - DETR: up to 10 car boxes, 0.62–0.96, plus truck 0.66
  - Faster R-CNN: 0.95
  - Mask R-CNN: 0.88
  - RetinaNet: 0.66
  - YOLO: 0.51
- Small extra persons on the reflected street: Faster R-CNN 0.79/0.64, Mask R-CNN 0.84/0.74, DETR 0.81, FCOS 0.53.
- Caveat: this is a glass reflection, not a wet surface.

*Caption:* A shop window reflects a city street, with parked vehicles and a pedestrian superimposed on the glass. All seven detectors report a person on the reflected pedestrian (0.76–1.00), and six of seven also report reflected vehicles as cars (up to 0.96).

### 4. mirror1_alt1 (mirror_b_child_side): child's face in a side mirror
**Fooled: 7/7.** All seven report "person" on the face in the mirror:
- DETR 1.00
- Faster R-CNN 0.98
- Mask R-CNN 0.97
- RetinaNet 0.83
- SSD 0.82
- FCOS 0.67 (+0.60, 0.57)
- YOLO 0.65

Other errors:
- "car" box over the mirror housing: DETR 0.73, Faster R-CNN 0.72, RetinaNet 0.54.
- "toothbrush" on the window edge, DETR only: 0.90, 0.53, 0.50.
- The real, blurred child in the foreground is found only by Mask R-CNN (0.89), DETR (0.87) and SSD (0.56).

*Caption:* A child's face is visible in a car's side mirror, while the child is out of focus in the foreground. All seven detectors report a person on the mirror image (0.65–1.00), whereas only three detect the blurred child (0.56–0.89). DETR additionally labels the window edge a toothbrush (0.90).

### 5. mirror1_alt2 (mirror_b_sidemasks): two masked people in a side mirror
**Fooled: 7/7.** All seven report "person" on one or both mirrored figures:
- DETR: 0.99, 0.98
- Mask R-CNN: 0.99, 0.97
- Faster R-CNN: 0.97, 0.95
- RetinaNet: 0.77, 0.65, 0.63
- SSD: 0.75
- FCOS: 0.68, 0.66
- YOLO: 0.63

Other errors:
- Whole frame or mirror labelled as a vehicle: DETR truck 0.87/0.75/0.65, YOLO bus 0.56, RetinaNet car 0.51.
- Inside the mirror: "bottle" (Mask R-CNN 0.98, Faster R-CNN 0.84, FCOS 0.80, DETR 0.75), Faster R-CNN baseball glove 0.62, and "cell phone" on the reflected phone (DETR 0.98, Faster R-CNN 0.90, Mask R-CNN 0.87, FCOS 0.62, RetinaNet 0.56).
- YOLO misses the real pedestrian on the road, which the other six detect (0.57–1.00).

*Caption:* A side mirror reflects two masked occupants, while a pedestrian walks on the road beyond. All seven detectors report persons inside the mirror (0.63–0.99). YOLO v11 detects only the mirrored person (0.63) and labels the mirror a bus (0.56), missing the real pedestrian.

### 6. mirror3_alt1 (mirror3_b_teen): face in a rear-view mirror
**Fooled: 6/7.** "Person" on the mirrored face:
- DETR 0.99 (+0.62)
- Faster R-CNN 0.99
- Mask R-CNN 0.98
- RetinaNet 0.70
- FCOS 0.67
- SSD 0.52

YOLO v11 returns no detections.

Other errors:
- Whole-frame "car": FCOS 0.64, Faster R-CNN 0.66 (two boxes), RetinaNet 0.53.
- Faster R-CNN "cup" 0.52 on the blurred building.

The README's 7/7 is not reproduced, because YOLO is empty.

*Caption:* Only a face reflected in a rear-view mirror is visible; nobody appears directly in the frame. Six of seven detectors report a person on the reflection (0.52–0.99). Three also label the whole windscreen view a car (0.53–0.66), and YOLO v11 returns no detections.

### 7. standee1_alt1 (standee_people_pose): Barack and Michelle Obama cardboard cutouts among visitors
**Fooled: 7/7** on the Michelle cutout:
- DETR 1.00
- Mask R-CNN 0.98
- Faster R-CNN 0.97
- SSD 0.90
- YOLO 0.80
- RetinaNet 0.75
- FCOS 0.70

**6/7** on the Barack cutout:
- Mask R-CNN 0.98
- Faster R-CNN 0.96
- DETR 0.95
- FCOS 0.61
- RetinaNet 0.61
- SSD 0.60
- YOLO does not detect it.

Other notes:
- "Tie" on the printed tie: DETR 0.99, Faster R-CNN 0.98, Mask R-CNN 0.95, FCOS 0.61, RetinaNet 0.54.
- The four real visitors are detected by all models.

*Caption:* Two life-size cardboard cutouts of Barack and Michelle Obama stand among four visitors. All seven detectors label the Michelle Obama cutout a person (0.70–1.00), and six of seven do the same for the Barack Obama cutout (0.60–0.98). Five models also detect the printed tie (0.54–0.99).

### 8. standee1_alt2 (standee_superman): Superman cutout in a waiting room
**Fooled: 7/7.** "Person" on the Superman cutout:
- DETR 1.00
- Faster R-CNN 1.00
- Mask R-CNN 1.00
- SSD 0.98
- YOLO 0.88
- RetinaNet 0.81
- FCOS 0.72

Other notes: the TV, chairs and people are detected normally. DETR and Faster R-CNN report a small "cell phone" (0.94, 0.54) on the woman standing to the right of the cutout.

*Caption:* A life-size Superman cardboard cutout stands among seated and standing people in a waiting area. All seven detectors classify the cutout as a person, with confidences of 0.72–1.00.

### 9. standee1_alt3 (standee_obama_ottawa1): visitor posing with an Obama cutout
**Fooled: 7/7.** "Person" on the cutout:
- DETR 1.00
- Faster R-CNN 1.00
- Mask R-CNN 1.00
- RetinaNet 0.94
- SSD 0.94
- YOLO 0.87
- FCOS 0.81

Other notes:
- "Tie" on the printed tie: DETR 1.00, Faster R-CNN 0.99, Mask R-CNN 0.99, FCOS 0.82, RetinaNet 0.66.
- RetinaNet adds a merged "person" 0.70 box spanning both figures.

*Caption:* A woman poses beside a life-size cardboard cutout of Barack Obama. All seven detectors label the cutout a person (0.81–1.00), with confidence comparable to the real woman, and five also detect its printed tie (0.66–1.00).

### 10. mannequin1_alt1 (mannequin_b_lying): mannequin lying on a plaza at night
**Fooled: 0/7** as "person". Two models mislabel the mannequin as an aeroplane: Faster R-CNN "airplane" 0.94 and Mask R-CNN "airplane" 0.84. The other five put no box on the mannequin. The distant real pedestrians are detected by all seven.

The README range "0.93–0.95" is wrong for Mask R-CNN (0.84).

*Caption:* A white mannequin lies on a paved plaza at night, with pedestrians in the background. No detector labels it a person; Faster R-CNN and Mask R-CNN classify it as an airplane (0.94 and 0.84), and the other five models ignore it.

### 11. mannequin1_alt2 (mannequin_b_pole): mannequin on a pavement beside a road
**Fooled: 7/7.** "Person" on the black-clad mannequin:
- DETR 1.00
- Mask R-CNN 1.00
- Faster R-CNN 0.99
- SSD 0.94
- YOLO 0.78
- RetinaNet 0.77
- FCOS 0.76

The clothing display on the right (pink shirt with cap) is also labelled person by all seven: DETR 0.99, Mask R-CNN 0.98, Faster R-CNN 0.96, SSD 0.92, FCOS 0.69, RetinaNet 0.65, YOLO 0.64.

Other errors:
- "Umbrella" on the mannequin's cap brim: Faster R-CNN 0.85, Mask R-CNN 0.70.
- Mask R-CNN "traffic light" 0.80 on a dark object above its head.
- "Handbag": DETR 0.75, 0.61.

*Caption:* A faceless mannequin dressed in black stands on a pavement beside a utility pole, with traffic behind it. All seven detectors classify it as a person (0.76–1.00), and all seven also report a person on a hanging clothing display to its right (0.64–0.99).

### 12. mannequin1_alt3 (mannequin1, Thirdman): silver mannequin beside a young man
**Fooled: 1/7.** RetinaNet labels the silver mannequin a person (0.52). The other six detect the man only: DETR 0.98, Faster R-CNN 0.99, Mask R-CNN 0.99, SSD 0.94, YOLO 0.82, FCOS 0.72. DETR's box (x from 826) partly covers the mannequin's arm.

Other errors:
- Mannequin labelled "vase": DETR 1.00, Mask R-CNN 0.83/0.67, Faster R-CNN 0.61/0.55.
- Mannequin labelled "bottle": Faster R-CNN 0.51.
- Faster R-CNN "tie" 0.61 on the man's open shirt.

*Caption:* A silver, faceless mannequin stands beside a young man under neon light. Only RetinaNet labels the mannequin a person (0.52). Three models instead call it a vase (DETR 1.00, Mask R-CNN 0.83, Faster R-CNN 0.61).

### 13. mannequin2_alt1 (mannequin2, Baranov): bridal mannequin in a display kiosk
**Fooled: 3/7.** "Person" on the mannequin behind glass: Mask R-CNN 0.91, DETR 0.85, Faster R-CNN 0.83 (+0.62). SSD, FCOS, RetinaNet and YOLO detect only the real woman.

Other errors:
- SSD "truck" 0.68 on the kiosk.
- A duplicate "person" on the woman's head: DETR 0.94, Faster R-CNN 0.92, Mask R-CNN 0.94, FCOS 0.65, RetinaNet 0.53.

*Caption:* A bridal mannequin is displayed inside a glass kiosk while an elderly woman stands nearby. Three of seven detectors label the mannequin a person (Mask R-CNN 0.91, DETR 0.85, Faster R-CNN 0.83). SSD labels the kiosk a truck (0.68).

### 14. painting3_alt1 (painting3_b1): street mural of a bearded man
**Fooled: 0/7** on the large mural face. No model reports a person on it. FCOS reports "umbrella" 0.55 on the beard, and Faster R-CNN reports "tennis racket" 0.90 at its lower edge.

A small painted figure of a girl on the wall (x around 130–175) does receive "person" from DETR 0.66, Faster R-CNN 0.71 and Mask R-CNN 0.78 (3/7). This was read from the tapestry and should be confirmed at full resolution.

Other errors: "cell phone" 0.53–0.99 (DETR) on the phone held by the walking man, which is correct.

*Caption:* Pedestrians walk past a large mural of a bearded man. No detector labels the mural a person; FCOS and Faster R-CNN instead report an umbrella (0.55) and a tennis racket (0.90) on it.

### 15. printed_poster_alt1 (printed_poster): two women passing a giant printed eye
**Fooled: 3/7.** "Person" boxes covering the poster: Mask R-CNN 0.85, Faster R-CNN 0.84, SSD 0.58. DETR, FCOS, RetinaNet and YOLO detect only the two women (0.77–1.00).

Other errors:
- Large boxes covering the women plus the poster: Faster R-CNN 0.80, Mask R-CNN 0.52.
- Duplicate "handbag" boxes: Faster R-CNN 0.57, Mask R-CNN 0.84.

*Caption:* Two women walk past a wall-sized printed close-up of an eye. All seven detectors find both women. Three also report a person spanning the printed face: Mask R-CNN 0.85, Faster R-CNN 0.84 and SSD 0.58.

### 16. blur_alt1 (blur): cars in a road tunnel
**Fooled: 2/7.**
- YOLO v11 detects only one small mid-distance car (0.71) and misses the two nearest cars, which every other model finds.
- SSD finds two cars (0.76, 0.61) but misses the smaller mid-distance ones.

Other errors: DETR adds "truck" 0.50 on a car it also labels car 1.00. The blur in this frame is mild.

*Caption:* Cars drive through a dimly lit road tunnel. Five of seven detectors find four to six vehicles (up to 1.00). YOLO v11 reports a single distant car (0.71) and misses the two closest vehicles, and SSD reports only two cars.

### 17. rain4_alt1 (rain4_b_pickup): pickup on a hazy storm road
**Fooled: 2/7.** SSD and YOLO v11 return no detections.

The other five find the pickup:
- DETR: car 1.00
- FCOS: truck 0.70 / car 0.52
- Faster R-CNN: truck 0.73
- RetinaNet: truck 0.67 / car 0.58
- Mask R-CNN: car 0.65 / truck 0.58

"Truck" is the COCO-correct class for a pickup. The README states that only SSD misses, but YOLO misses too.

*Caption:* A pickup truck drives along a road in thick haze. Five detectors find it as car or truck (0.58–1.00). SSD and YOLO v11 return no detections at all.

### 18. fog1_alt1 (fog1, Podzolkin): lone figure on a foggy path
**Fooled: 2/7.** SSD and YOLO v11 return no detections. The other five report "person": DETR 1.00, Mask R-CNN 1.00, Faster R-CNN 0.99, RetinaNet 0.66, FCOS 0.61. No model reports a bicycle, although the source title says a bike is present. This cannot be confirmed at tapestry resolution.

*Caption:* A single small figure stands on a path in dense fog. Five detectors find the person (0.61–1.00), while SSD and YOLO v11 return no detections.

### 19. fog1_alt2 (fog1_b_pexcyclist): cyclist on a foggy bridge
**Fooled: 2/7.** All seven detect the rider as a person (0.78–1.00), but SSD and YOLO v11 miss the bicycle. YOLO reports only person 0.78 and backpack 0.55. The other five find the bicycle (0.67–1.00).

Other notes: RetinaNet adds a duplicate person (0.52), and Mask R-CNN a second backpack (0.54). Distant cars are found by most models.

*Caption:* A cyclist rides across a steel bridge in fog. All seven detectors find the rider (0.78–1.00), but SSD and YOLO v11 do not detect the bicycle, which the other five report at 0.67–1.00.

### 20. fog1_alt3 (fog_b_bridge_night): pedestrians and a car on a bridge in night fog
**Fooled: 3/7.**
- Phantom "person" on the dark bridge pillar at the left edge: DETR 0.51, Faster R-CNN 0.63.
- SSD detects only one of the pedestrians (0.52).

Every model detects the car (0.53–0.97). The pedestrians are found by the other models (0.60–1.00).

*Caption:* Pedestrians walk along a bridge in night fog as a car approaches with its headlights on. All detectors find the car. DETR and Faster R-CNN additionally report a person on the dark bridge pillar (0.51, 0.63), and SSD detects only one pedestrian (0.52).

### 21. fog2_alt1 (fog2_b_moto3): two motorcycles with headlights in fog
**Fooled: 2/7.**
- SSD reports only the near rider (person 0.82) and misses both motorcycles and the far rider.
- YOLO v11 reports the near rider and motorcycle (0.61, 0.76) and misses the far pair.

Other errors: Mask R-CNN adds "boat" 0.52 on the far motorcycle, which it also labels motorcycle 0.73. RetinaNet adds a duplicate motorcycle (0.50).

*Caption:* Two motorcyclists ride towards the camera on a foggy road at dusk. Five detectors find both riders and both motorcycles. SSD detects only the nearer rider (0.82), and YOLO v11 misses the farther motorcycle and rider entirely.

### 22. fog2_alt2 (fog2, Bringas): motorcyclist and cars on a foggy highway, seen from inside a car
**Fooled: 3/7.**
- Faster R-CNN and Mask R-CNN report a phantom "car" on the host car's dashboard (0.67, 0.65).
- SSD gives one person box over the rider and machine (0.63) with no motorcycle label, and misses one of the cars.

Other errors:
- "Truck" on a car that is also labelled car: Faster R-CNN 0.65, FCOS 0.51.
- FCOS "backpack" 0.54 on the motorcycle.
- The hanging air freshener is ignored by all models.

*Caption:* A motorcyclist rides between cars on a foggy highway, photographed through a windscreen. All detectors find the main cars. Faster R-CNN and Mask R-CNN also report a car on the dashboard (0.67, 0.65), and SSD does not detect the motorcycle.
