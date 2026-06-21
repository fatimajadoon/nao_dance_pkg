# nao_dance_pkg

**NAO Humanoid Robot Dance Routine — Webots**

A choreographed 5-movement dance routine for the NAO H25 V5.0 robot
performed in a stadium environment.

---

## Dance Routine Summary

| # | Movement | Limbs | Motion File |
|---|---|---|---|
| 1 | Hand Wave | Right arm | HandWave.motion (pre-built) |
| 2 | Tai Chi | Both arms + both legs + torso | TaiChi.motion (pre-built) |
| 3 | Side Step Shuffle (×3) | Both legs + arms | SideStepLeft + SideStepRight (pre-built, sequenced) |
| 4 | Spin Turn (×2) | Both legs + arms + torso | TurnLeft60 + TurnRight60 (pre-built, sequenced) |
| 5 | Wipe & Shoot Finale | Right arm + head + left leg | WipeForehead + Shoot (pre-built, sequenced) |

**Declaration:** All individual motion sequences use pre-built `.motion` files
provided by Cyberbotics/Webots for the NAO robot. The choreography,
sequencing, timing, repetition logic, and LED visual effects are original
work by the author.

---

## How to Run

```bash
export WEBOTS_HOME=/usr/local/webots
webots ~/dance_ws/src/nao_dance_pkg/worlds/nao_dance_stadium.wbt
```

---

## Git Commit History

```
commit 1  — "Initial commit: create ROS 2 package skeleton"
commit 2  — "Add stadium world with NAO robot at centre stage"
commit 3  — "Add controller scaffold: motion loading and LED init"
commit 4  — "Implement Movement 1: Hand Wave (right arm)"
commit 5  — "Implement Movement 2: Tai Chi (both arms and legs)"
commit 6  — "Implement Movement 3: Side Step Shuffle (both legs x3)"
commit 7  — "Implement Movement 4: Spin Turn full body rotation x2"
commit 8  — "Implement Movement 5: Wipe and Shoot finale"
commit 9  — "Add LED colour effects and flash sequences per movement"
commit 10 — "Final tidy-up: add repeat logic, logging, and README"
```

---

## GitHub
https://github.com/fatimajadoon/nao_dance_pkg

---

## License
MIT
