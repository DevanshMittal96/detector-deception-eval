# Image Sources

> **Copyright Notice:** The images used in this study are sourced from third-party
> websites and are the property of their respective copyright holders. We do not
> redistribute the images themselves. The links below point to the original sources
> from which each image can be accessed. Some links may become unavailable over time
> as source websites update their content.

## How to Use

1. Visit each link below and download the image manually.
2. Place all downloaded images into the `images/` directory.
3. Run the pipeline: `python run_detectors.py --input ./images --output ./results`

You may rename the files as you wish — the pipeline processes all supported formats
(`.jpg`, `.jpeg`, `.png`, `.webp`, `.avif`, `.bmp`, `.tiff`) found in the input
directory.

---

## Category 1 — Optical-Geometric Distortions (Mirrors & Reflections)

These images feature rearview mirrors, reflective surfaces, and specular geometries
that can produce phantom object detections.

| # | Source |
|---|--------|
| 1 | https://www.westend61.de/en/photo/PNAF03895/smiling-man-looking-in-rear-view-mirror-of-car |
| 2 | https://www.123rf.com/photo_130125310_closeup-of-reflection-of-woman-and-man-in-the-rearview-mirror-while-they-travelling-by-car.html |
| 3 | https://www.amazon.com/Ideapro-Backseat-Rearview-Adjustable-Forward/dp/B01N0AXQLN |
| 4 | https://x.com/quackity4k/status/1866565504502218823 |

---

## Category 2 — Anthropomorphic Mimicry (Mannequins)

These images contain mannequins alongside real people, probing whether detectors
can discriminate between live persons and human surrogates.

| # | Source |
|---|--------|
| 5 | https://www.pexels.com/photo/elderly-man-in-brown-vest-standing-beside-a-mannequin-in-gray-suit-6050442/ |
| 6 | https://www.dreamstime.com/confident-young-fashion-designer-posing-next-to-mannequin-exclusive-custom-made-men-s-suit-dark-tailor-elegantly-dressed-image138672922 |
| 7 | https://www.alamy.com/young-handsome-man-and-pretty-woman-couple-designer-has-conflict-together-while-use-laptop-computer-chatting-with-customer-online-order-mannequin-image640326498.html |

---

## Category 3 — Anthropomorphic Mimicry (Posters & Printed Faces)

These images feature movie posters, celebrity photographs, and large-format printed
faces that may trigger false "person" detections.

| # | Source |
|---|--------|
| 8 | https://in.pinterest.com/pin/the-music-launch-of-mudda-370-jk--568438784218162989/ |
| 9 | https://www.gettyimages.in/detail/news-photo/kevin-hart-stands-next-to-a-poster-in-the-lobby-for-the-news-photo/488732849 |
| 10 | https://www.gettyimages.ae/detail/news-photo/actor-ron-rifkin-stands-beside-a-poster-promoting-the-news-photo/785415 |

---

## Category 4 — Anthropomorphic Mimicry (Celebrity T-Shirts)

These images show people wearing T-shirts bearing celebrity faces, testing whether
detectors register the printed face as an additional person.

| # | Source |
|---|--------|
| 11–12 | https://www.indiatoday.in/entertainment/photo/celebrity-face-t-shirts-latest-trend-in-hollywood-372216-2014-05-15/6 |
| 13 | https://abcnews.go.com/Entertainment/trend-celebrities-wearing-shirts-celebs/story?id=24108637 |

---

## Category 5 — Anthropomorphic Mimicry (Paintings & Portraits)

These images contain paintings or portrait art of people, probing whether detectors
distinguish between real persons and artistic depictions.

| # | Source |
|---|--------|
| 14 | https://www.pinterest.com/pin/28429041372815454/ |
| 15 | https://www.bethanturnerportraitartist.co.uk/about-the-artist.html |
| 16–17 | https://newsforkids.net/articles/2019/02/06/a-painting-of-a-painting-of-a-painting/ |

---

## Category 6 — Anthropomorphic Mimicry (Life-Size Cardboard Cutouts)

These images feature life-size cardboard standees of political figures and
celebrities, testing detector responses to full-body human surrogates.

| # | Source |
|---|--------|
| 18 | https://www.tribuneindia.com/news/j-k/pm-modis-life-size-cutout-draws-visitors-to-srinagars-lal-chowk-562927/ |
| 19 | https://www.alamy.com/a-man-carries-a-life-size-cutout-photo-of-indian-prime-minister-narendra-modi-during-his-roadshow-before-inaugurating-a-new-airport-and-a-railway-station-in-ayodhya-india-saturday-dec-30-2023-ap-photorajesh-kumar-singh-image591215753.html |
| 20 | https://www.gettyimages.com.au/detail/news-photo/cardboard-cutouts-greet-guests-as-they-arrive-at-the-old-news-photo/2159604263 |
| 21 | https://www.alamy.com/a-man-holds-a-life-size-cardboard-of-britains-king-charles-iii-and-camilla-queen-consort-along-the-kings-coronation-route-at-the-mall-in-london-thursday-may-4-2023-the-coronation-of-king-charles-iii-will-take-place-at-westminster-abbey-on-may-6-ap-photoandreea-alexandru-image550571563.html |
| 22 | https://www.gettyimages.com.au/detail/news-photo/thomas-quaas-chairman-of-german-consumer-chemicals-and-news-photo/97424878 |
| 23 | https://www.gettyimages.com.au/detail/news-photo/turkish-party-activist-holds-a-cardboard-cutout-of-news-photo/974138756 |

---

## Category 7 — Environmental Degradation (Fog)

These images depict driving scenes under dense fog, where atmospheric scattering
degrades visibility and causes missed detections.

| # | Source |
|---|--------|
| 24 | https://auto.hindustantimes.com/how-to/how-to-drive-safely-in-foggy-weather-key-tips-41671522073142.html |
| 25 | https://auto.hindustantimes.com/auto/news/winter-foggy-weather-is-posing-a-danger-of-car-pileups-on-highways-how-to-drive-safe-41732504753405.html |
| 26 | https://advanced-driving.co.uk/driving-blog/tips-for-driving-in-fog/ |
| 27 | https://www.news18.com/auto/driving-in-dense-fog-this-winter-these-tips-will-help-you-stay-safe-ws-ab-9198771.html |

---

## Category 8 — Environmental Degradation (Rain & Wet Surfaces)

These images capture driving in heavy rain and wet road conditions, where raindrops
on the windshield and specular reflections on wet asphalt challenge detectors.

| # | Source |
|---|--------|
| 28 | https://driveredsafety.com/safely-drive-rain/ |
| 29 | https://www.rozoninsurance.ca/blog/6-tips-for-driving-in-the-rain/ |
| 30 | https://www.scottclarkstoyota.com/blogs/207/5-tips-driving-heavy-rain/ |
| 31 | https://www.lindleysautocentres.co.uk/about-us/blog/8-tips-for-driving-in-heavy-rain/ |

---

## Category 9 — Environmental Degradation (Tunnels & Low Light)

These images depict vehicles in dark tunnels with wet surfaces, combining low-light
conditions with specular reflections.

| # | Source |
|---|--------|
| 32 | https://www.dreamstime.com/cars-driving-wet-tunnel-night-image344214201 |
| 33 | https://www.dreamstime.com/cars-driving-dark-tunnel-red-taillights-image344214390 |
