#!/usr/bin/env python3

# nao_dance.py
# Author: Fatima Jadoon
# Date: April 2026
#
# Webots Python controller for the NAO humanoid robot.
# Implements a choreographed dance routine in a stadium environment.
#
# The dance routine consists of 5 movements:
#
#   Movement 1 — Hand Wave (right arm)
#     The robot waves its right hand as an opening gesture.
#     Uses: HandWave.motion (pre-built)
#
#   Movement 2 — Tai Chi (both arms + legs + torso)
#     A slow flowing sequence involving both arms and legs simultaneously.
#     This is the most complex movement involving the most limbs.
#     Uses: TaiChi.motion (pre-built)
#
#   Movement 3 — Side Step Shuffle (both legs)
#     The robot steps left then right repeatedly in a shuffling dance move.
#     Involves both legs alternating weight transfer.
#     Uses: SideStepLeft.motion + SideStepRight.motion (pre-built, sequenced)
#
#   Movement 4 — Spin Turn (full body rotation)
#     The robot turns left 60 degrees then right 60 degrees twice,
#     creating a spinning dance effect involving the full body.
#     Uses: TurnLeft60.motion + TurnRight60.motion (pre-built, sequenced)
#
#   Movement 5 — Wipe and Shoot Finale (arms + legs)
#     The robot wipes its forehead then performs a kick/shoot motion
#     as a dramatic finale. Involves both arms and kicking leg.
#     Uses: WipeForehead.motion + Shoot.motion (pre-built, sequenced)
#
# DECLARATION:
#   All motion sequences use pre-built .motion files provided by
#   Cyberbotics/Webots for the NAO robot. These files contain
#   keyframe joint angle sequences validated on the real NAO robot.
#   The choreography, sequencing, timing, repetition logic, and
#   LED visual effects are original work by the author.
#
# The routine loops continuously so it can be recorded easily.

import sys
import os
import time

WEBOTS_HOME = os.environ.get('WEBOTS_HOME', '/usr/local/webots')
sys.path.append(os.path.join(WEBOTS_HOME, 'lib', 'controller', 'python'))

from controller import Robot, Motion

# Path to the NAO motion files
MOTIONS_PATH = '../../motions/'

# How many times to repeat the full dance routine before stopping
# Set to 0 for infinite loop
REPEAT_COUNT = 3


class NaoDance(Robot):
    """
    NAO robot dance controller.
    Plays a choreographed sequence of 5 movements involving
    multiple limbs simultaneously, using pre-built motion files.
    The routine includes arm waves, tai chi, side steps,
    spin turns, and a finale kick.
    """

    def __init__(self):
        super().__init__()
        self.time_step = int(self.getBasicTimeStep())

        print("=" * 55)
        print("NAO Dance Controller")
        print("Author: Fatima Jadoon")
        print("Routine: 5-movement Stadium Dance")
        print("=" * 55)

        # ---- Load all motion files ----
        self._load_motions()

        # ---- Initialise LEDs for visual effects ----
        self._init_leds()

        # ---- State tracking ----
        self.currently_playing = None
        self.routine_count     = 0

        print("Controller ready. Starting dance routine...\n")

    # -----------------------------------------------------------------------
    # Motion file loading
    # -----------------------------------------------------------------------

    def _load_motions(self):
        """
        Load all pre-built NAO motion files used in the dance routine.
        These are official Webots/Cyberbotics motion files containing
        validated joint angle keyframe sequences.
        """
        try:
            self.motion_handwave     = Motion(MOTIONS_PATH + 'HandWave.motion')
            self.motion_taichi       = Motion(MOTIONS_PATH + 'TaiChi.motion')
            self.motion_step_left    = Motion(MOTIONS_PATH + 'SideStepLeft.motion')
            self.motion_step_right   = Motion(MOTIONS_PATH + 'SideStepRight.motion')
            self.motion_turn_left    = Motion(MOTIONS_PATH + 'TurnLeft60.motion')
            self.motion_turn_right   = Motion(MOTIONS_PATH + 'TurnRight60.motion')
            self.motion_wipe         = Motion(MOTIONS_PATH + 'WipeForehead.motion')
            self.motion_shoot        = Motion(MOTIONS_PATH + 'Shoot.motion')
            self.motion_forwards     = Motion(MOTIONS_PATH + 'Forwards50.motion')

            print("Motion files loaded:")
            print("  HandWave, TaiChi, SideStepLeft, SideStepRight,")
            print("  TurnLeft60, TurnRight60, WipeForehead, Shoot, Forwards50")

        except Exception as e:
            print(f"Error loading motion files: {e}")
            sys.exit(1)

    # -----------------------------------------------------------------------
    # LED initialisation
    # -----------------------------------------------------------------------

    def _init_leds(self):
        """Initialise LEDs for visual dance effects."""
        try:
            self.chest_led  = self.getDevice('ChestBoard/Led')
            self.lfoot_led  = self.getDevice('LFoot/Led')
            self.rfoot_led  = self.getDevice('RFoot/Led')
            self.face_led_r = self.getDevice('Face/Led/Right')
            self.face_led_l = self.getDevice('Face/Led/Left')
            self.ear_led_r  = self.getDevice('Ears/Led/Right')
            self.ear_led_l  = self.getDevice('Ears/Led/Left')
            self.leds_ready = True
            print("LEDs initialised for visual effects.")
        except Exception:
            self.leds_ready = False
            print("LEDs not available — continuing without visual effects.")

    def set_leds(self, color):
        """Set all LEDs to a given RGB colour."""
        if not self.leds_ready:
            return
        try:
            self.chest_led.set(color)
            self.lfoot_led.set(color)
            self.rfoot_led.set(color)
            self.face_led_r.set(color)
            self.face_led_l.set(color)
            self.ear_led_r.set(color & 0xFF)
            self.ear_led_l.set(color & 0xFF)
        except Exception:
            pass

    def flash_leds(self, color1, color2, times=3):
        """Flash LEDs between two colours for visual effect."""
        for _ in range(times):
            self.set_leds(color1)
            self.wait(200)
            self.set_leds(color2)
            self.wait(200)

    # -----------------------------------------------------------------------
    # Motion control
    # -----------------------------------------------------------------------

    def play_motion(self, motion):
        """
        Start a motion, stopping any currently playing motion first.
        """
        if self.currently_playing and not self.currently_playing.isOver():
            self.currently_playing.stop()
        motion.play()
        self.currently_playing = motion

    def wait_for_motion(self, motion):
        """
        Block until the given motion finishes.
        Steps the simulation on each iteration.
        """
        while not motion.isOver():
            if self.step(self.time_step) == -1:
                sys.exit(0)

    def play_and_wait(self, motion, label=""):
        """Play a motion and wait for it to complete with logging."""
        if label:
            print(f"  >> Playing: {label}")
        self.play_motion(motion)
        self.wait_for_motion(motion)

    # -----------------------------------------------------------------------
    # Timing utility
    # -----------------------------------------------------------------------

    def wait(self, ms):
        """Wait for a given number of milliseconds in simulation time."""
        start = self.getTime()
        while self.getTime() - start < ms / 1000.0:
            if self.step(self.time_step) == -1:
                sys.exit(0)

    # -----------------------------------------------------------------------
    # Dance movements
    # -----------------------------------------------------------------------

    def movement_1_hand_wave(self):
        """
        Movement 1: Hand Wave
        The robot waves its right hand as an opening greeting gesture.
        Limbs involved: right arm (shoulder, elbow, wrist joints)
        Duration: ~3 seconds
        Pre-built motion: HandWave.motion
        """
        print("\n[MOVEMENT 1] Hand Wave — Opening greeting")
        print("  Limbs: Right arm (shoulder, elbow, wrist)")
        self.set_leds(0x00FF00)  # green = friendly wave

        self.play_and_wait(self.motion_handwave, "HandWave.motion")

        print("  Movement 1 complete.")

    def movement_2_tai_chi(self):
        """
        Movement 2: Tai Chi
        A slow, flowing sequence involving both arms, both legs, and the torso.
        This is the most expressive movement in the routine, demonstrating
        smooth coordinated multi-limb control.
        Limbs involved: both arms, both legs, torso rotation
        Duration: ~15 seconds
        Pre-built motion: TaiChi.motion
        """
        print("\n[MOVEMENT 2] Tai Chi — Flowing multi-limb sequence")
        print("  Limbs: Both arms, both legs, torso")
        self.set_leds(0x0000FF)  # blue = calm, flowing

        self.play_and_wait(self.motion_taichi, "TaiChi.motion")

        print("  Movement 2 complete.")

    def movement_3_side_shuffle(self):
        """
        Movement 3: Side Step Shuffle
        The robot alternates stepping left and right three times,
        creating a classic dance shuffle. Both legs are involved
        in transferring weight and stepping sideways.
        Limbs involved: both legs, arms swing for balance
        Duration: ~9 seconds (3 left + 3 right steps)
        Pre-built motions: SideStepLeft.motion + SideStepRight.motion (sequenced)
        """
        print("\n[MOVEMENT 3] Side Step Shuffle — Alternating steps")
        print("  Limbs: Both legs (weight transfer), arms (balance)")
        self.set_leds(0xFF6600)  # orange = energetic shuffle

        # Three left-right shuffle cycles
        for i in range(3):
            print(f"  Shuffle cycle {i+1}/3...")
            self.play_and_wait(self.motion_step_left,  "SideStepLeft.motion")
            self.play_and_wait(self.motion_step_right, "SideStepRight.motion")

        print("  Movement 3 complete.")

    def movement_4_spin_turn(self):
        """
        Movement 4: Spin Turn
        The robot turns left 60 degrees then right 60 degrees twice,
        creating a spinning dance effect. Involves full-body rotation
        with both legs stepping and arms balancing.
        Limbs involved: both legs (stepping), both arms (balance), torso
        Duration: ~8 seconds
        Pre-built motions: TurnLeft60.motion + TurnRight60.motion (sequenced)
        """
        print("\n[MOVEMENT 4] Spin Turn — Full body rotation")
        print("  Limbs: Both legs (stepping), both arms (balance), torso")
        self.flash_leds(0xFF0000, 0xFFFFFF, times=3)  # flash red/white = dramatic spin
        self.set_leds(0xFF0000)

        # Two spin cycles: left then right
        for i in range(2):
            print(f"  Spin cycle {i+1}/2...")
            self.play_and_wait(self.motion_turn_left,  "TurnLeft60.motion")
            self.play_and_wait(self.motion_turn_right, "TurnRight60.motion")

        print("  Movement 4 complete.")

    def movement_5_finale(self):
        """
        Movement 5: Wipe and Shoot Finale
        A two-part finale: the robot wipes its forehead (right arm + head tilt)
        then performs a dramatic kick/shoot motion (left leg kick + arm swing).
        Limbs involved: right arm, head, left leg, both arms
        Duration: ~6 seconds
        Pre-built motions: WipeForehead.motion + Shoot.motion (sequenced)
        """
        print("\n[MOVEMENT 5] Wipe and Shoot Finale — Grand finale!")
        print("  Limbs: Right arm + head (wipe), Left leg + arms (shoot)")
        self.flash_leds(0xFF00FF, 0xFFFF00, times=5)  # flash purple/yellow = finale!
        self.set_leds(0xFF00FF)

        self.play_and_wait(self.motion_wipe,  "WipeForehead.motion")
        self.wait(300)  # brief dramatic pause between the two finale moves
        self.play_and_wait(self.motion_shoot, "Shoot.motion")

        # Victory flash at the end
        self.flash_leds(0xFFFFFF, 0x000000, times=5)
        self.set_leds(0x00FF00)

        print("  Movement 5 complete — Routine finished!")

    # -----------------------------------------------------------------------
    # Full dance routine
    # -----------------------------------------------------------------------

    def perform_routine(self):
        """
        Performs the complete 5-movement dance routine in sequence.
        Logs the start and end time of each movement.
        """
        self.routine_count += 1
        print(f"\n{'='*55}")
        print(f"DANCE ROUTINE — Performance {self.routine_count}")
        print(f"Time: {self.getTime():.1f}s")
        print(f"{'='*55}")

        # Opening LED sequence
        self.flash_leds(0xFF0000, 0x00FF00, times=3)
        self.wait(500)

        # Execute all 5 movements in sequence
        self.movement_1_hand_wave()
        self.wait(500)

        self.movement_2_tai_chi()
        self.wait(500)

        self.movement_3_side_shuffle()
        self.wait(500)

        self.movement_4_spin_turn()
        self.wait(500)

        self.movement_5_finale()
        self.wait(1000)

        print(f"\n[ROUTINE {self.routine_count}] Complete at t={self.getTime():.1f}s")

    # -----------------------------------------------------------------------
    # Main loop
    # -----------------------------------------------------------------------

    def run(self):
        """
        Main control loop. Performs the dance routine REPEAT_COUNT times.
        If REPEAT_COUNT is 0, loops indefinitely.
        """
        # Advance one step to initialise sensors
        if self.step(self.time_step) == -1:
            sys.exit(0)

        print("\n[INIT] NAO robot ready in stadium.")
        print(f"[INIT] Will perform {REPEAT_COUNT if REPEAT_COUNT > 0 else 'infinite'} "
              f"routine(s).\n")

        # Brief pause before starting
        self.wait(1000)

        count = 0
        while True:
            self.perform_routine()

            count += 1
            if REPEAT_COUNT > 0 and count >= REPEAT_COUNT:
                print(f"\n[DONE] All {REPEAT_COUNT} routines complete. Robot standing by.")
                self.set_leds(0xFFFFFF)
                # Keep simulation running
                while True:
                    if self.step(self.time_step) == -1:
                        sys.exit(0)

            # Brief pause between routines
            self.wait(2000)
            print("\n[REPEAT] Starting next routine...\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    robot = NaoDance()
    robot.run()


if __name__ == '__main__':
    main()
