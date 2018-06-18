import sys
import random
import time
import pygame
from pets import BattleState, BattleResult, SkillType, Skill, Pet
from image import *


class Battle:
    def __init__(self, screen, player, enermy_pets):
        self.screen = screen
        self.pet_width = (self.screen.get_width() - 40) / 4
        self.pet_height = 80
        self.button_width = self.screen.get_width() / 2
        self.button_height = 80
        self.bar_height = 15
        self.background_image = pygame.image.load("resources\\images\\background.png").convert()

        self.button_image_startx = 0
        self.button_image_starty = self.screen.get_height() - 3 * self.button_height
        self.enermy_bar_startx = 20
        self.enermy_bar_starty = 20
        self.enermy_image_startx = self.enermy_bar_startx
        self.enermy_image_starty = self.bar_height + self.enermy_bar_starty
        self.friend_image_startx = self.screen.get_width() - 80 - 20
        self.friend_image_starty = self.button_image_starty - self.pet_height - self.bar_height

        self.player = player
        self.friend_pets = player.battle_list
        self.enermy_pets = enermy_pets
        self.killed_enermys = []

        self.friend_pet_images = []
        self.enermy_pet_images = []
        self.enermy_hp_bars = []
        self.button_images = []

        self.hp_bar = BarImage(self.screen, self.screen.get_width() / 2, self.bar_height, (255, 0, 0),
                               (255, 255, 255), "HP", 24, self.player.max_hp, self.player.hp)
        self.mp_bar = BarImage(self.screen, self.screen.get_width() / 2, self.bar_height, (0, 0, 255),
                               (255, 255, 255), "MP", 24, self.player.max_mp, self.player.mp)

        self.create_buttons()
        self.update_screen()
        self.draw_screen()

        self.battle_state = BattleState.SelectAction
        self.battle_result = BattleResult.Match
        self.battle_region = 0
        self.battle_continue = False
        self.want_escape = False
        self.skill_index = 0
        self.skill_type = SkillType.NormalAttack
        self.skill_effort = 0
        self.skill_cost = 0
        self.select_enermy = 0

    def start_battle(self):
        if self.player.hp <= 0:
            print("Player seriously injured, could not enter a battle!!!")
            return
        while True:
            self.check_events()
            self.execute_state()
            self.update_screen()
            self.draw_screen()
            if BattleResult.Victory == self.battle_result or self.battle_result == BattleResult.Defeat or \
                    self.battle_result == BattleResult.Escape:
                if BattleResult.Victory:
                    self.gain_reward()
                break
            pygame.display.flip()

    def gain_reward(self):
        for killed_enermy in self.killed_enermys:
            self.player.gain_exp(killed_enermy.beated_exp)
            self.player.gain_money(killed_enermy.beated_money)
            for pet in self.player.battle_list:
                pet.gain_exp(killed_enermy.beated_exp)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.battle_region = self.check_region(event.pos)
                    self.click_button()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.release_button()

    def execute_state(self):
        if self.battle_continue:
            print(self.battle_state)
            if self.battle_state == BattleState.SelectAction:
                print("\tSelected Button:\t", self.battle_region)
                if self.battle_region == 0:
                    self.skill_type = SkillType.NormalAttack
                    self.skill_effort = self.player.get_damage()
                    self.battle_state = BattleState.SelectEnermy
                    self.battle_continue = False
                elif self.battle_region == 1:
                    self.skill_type = SkillType.CatchPet
                    self.skill_effort = 0
                    self.battle_state = BattleState.SelectEnermy
                    self.battle_continue = False
                elif self.battle_region == 2:
                    self.want_escape = True
                    self.battle_state = BattleState.EnermyRound
                    self.battle_continue = True
                else:
                    skill_index = self.battle_region - 3
                    if len(self.friend_pets) > skill_index and self.player.get_skill_available(skill_index):
                        self.skill_type, self.skill_effort, self.skill_cost = self.player.get_skill_info(skill_index)
                        print("***", self.skill_effort)
                        print("\tSkill Type: ", self.skill_type)
                        print("\tSkill Effort", self.skill_effort)
                        print("\tSkill Cost:\t", self.skill_cost)
                        if self.skill_type == SkillType.AreaDamage or self.skill_type == SkillType.Heal:
                            self.battle_state = BattleState.FriendRound
                            self.battle_continue = True
                        else:
                            self.battle_state = BattleState.SelectEnermy
                            self.battle_continue = False
                    else:
                        print("\tPlayer MP:\t", self.player.mp_left)
                        print("\tMP Not Enough!")
                        self.battle_continue = False
            elif self.battle_state == BattleState.SelectEnermy:
                print("\tSelected Enermy:\t", self.battle_region)
                self.select_enermy = self.battle_region
                self.battle_state = BattleState.FriendRound
                self.battle_continue = True
            elif self.battle_state == BattleState.FriendRound:
                if self.skill_type == SkillType.NormalAttack:
                    self.friend_attack()
                    self.enermy_pets[self.select_enermy].take_damage(self.skill_effort)
                    print("\tEnermy Index: ", self.select_enermy)
                    print("\tEnermy HP: ", self.enermy_pets[self.select_enermy].pet_hp_left)
                    if not self.enermy_pets[self.select_enermy].is_alive():
                        print("\tEnermy ", self.enermy_pets[self.select_enermy].get_name(), " die.")
                        self.killed_enermys.append(self.enermy_pets[self.select_enermy])
                        del(self.enermy_pets[self.select_enermy])
                elif self.skill_type == SkillType.DirectDamage:
                    self.player.use_skill(self.skill_index)
                    self.friend_attack()
                    self.enermy_pets[self.select_enermy].take_damage(self.skill_effort)
                    print("\tEnermy Index: ", self.select_enermy)
                    print("\tEnermy HP: ", self.enermy_pets[self.select_enermy].pet_hp)
                    if not self.enermy_pets[self.select_enermy].is_alive():
                        print("\tEnermy ", self.enermy_pets[self.select_enermy].get_name(), " die.")
                        self.killed_enermys.append(self.enermy_pets[self.select_enermy])
                        del(self.enermy_pets[self.select_enermy])
                elif self.skill_type == SkillType.AreaDamage:
                    self.player.use_skill(self.skill_index)
                    self.friend_attack()
                    for i in range(len(self.enermy_pets)):
                        self.enermy_pets[i].take_damage(self.skill_effort)
                        print("\tEnermy Index: ", i)
                        print("\tEnermy HP: ", self.enermy_pets[i].pet_hp)
                    while True:
                        finish = True
                        for i in range(len(self.enermy_pets)):
                            if not self.enermy_pets[i].is_alive():
                                print("\tEnermy ", self.enermy_pets[i].get_name(), " die.")
                                self.killed_enermys.append(self.enermy_pets[self.select_enermy])
                                del(self.enermy_pets[i])
                                finish = False
                                break
                        if finish:
                            break
                elif self.skill_type == SkillType.Heal:
                    self.player.use_skill(self.skill_index)
                    print("\tPlayer HP: ", self.player.hp)
                    self.player.take_heal(self.skill_effort)
                elif self.skill_type == SkillType.CatchPet:
                    judge = random.randint(0, 10)
                    print("\tJudge Num:\t", judge)
                    if judge < 10:
                        print("\tCatch Successful!")
                        self.player.own_list.append(self.enermy_pets[self.select_enermy])
                        del (self.enermy_pets[self.select_enermy])
                        print("\tPlayer Own list:")
                        for pet in self.player.own_list:
                            print("\t\t", pet.get_name())
                    else:
                        print("\tCatch Fail!")
                else:
                    pass

                if len(self.enermy_pets ) == 0:
                    self.battle_state = BattleState.SelectAction
                    self.battle_result = BattleResult.Victory
                    return
                else:
                    self.battle_state = BattleState.EnermyRound
                    self.battle_continue = True
            elif self.battle_state == BattleState.EnermyRound:
                for i in range(len(self.enermy_pets)):
                    self.enermy_attack(i)
                    self.player.take_damage(self.enermy_pets[i].get_damage())
                    print("\tPlayer HP:\t", self.player.hp)
                    if self.player.hp == 0:
                        self.battle_result = BattleResult.Defeat
                        return
                if self.want_escape:
                    self.battle_state = BattleState.EscapeJudge
                    self.battle_continue = True
                else:
                    self.battle_state = BattleState.SelectAction
                    self.battle_continue = False
            else:
                judge = random.randint(0, 10)
                print("\tJudge Num:\t", judge)
                if judge < 6:
                    self.battle_result = BattleResult.Escape
                    print("\tEscape Successful!")
                    return
                else:
                    self.battle_result = BattleResult.Match
                    self.battle_state = BattleState.SelectAction
                    self.battle_continue = False
                    print("\tEscape Fail!")

    def check_region(self, pos):
        if self.battle_state == BattleState.SelectAction:
            for i in range(len(self.button_images)):
                if self.button_images[i].rect.collidepoint(pos):
                    print("Selected Region:\t", (0, i))
                    self.battle_continue = True
                    return i
        elif self.battle_state == BattleState.SelectEnermy:
            for i in range(len(self.enermy_pet_images)):
                if self.enermy_pet_images[i].rect.collidepoint(pos):
                    print("Selected Region:\t", (1, i))
                    self.battle_continue = True
                    return i
        else:
            return None

    def create_buttons(self):
        button = ButtonImage(self.screen, self.button_width, self.button_height, "resources\\images\\button1.png", "Attack", 24)
        self.button_images.append(button)
        button = ButtonImage(self.screen, self.button_width, self.button_height, "resources\\images\\button2.png", "Catch", 24)
        self.button_images.append(button)
        button = ButtonImage(self.screen, self.button_width, self.button_height, "resources\\images\\button3.png", "Escape", 24)
        self.button_images.append(button)
        for i in range(len(self.friend_pets)):
            button = ButtonImage(self.screen, self.button_width, self.button_height, "resources\\images\\button"+str(i+4)+".png",
                                 self.friend_pets[i].get_skill().skill_name + "(" + str(self.friend_pets[i].level) +  ")", 24)
            self.button_images.append(button)

    def update_screen(self):
        self.friend_pet_images = []
        self.enermy_pet_images = []
        self.enermy_hp_bars = []

        for i in range(len(self.enermy_pets)):
            pet_image = PetImage(self.screen, self.enermy_pets[i].pet_file, self.enermy_pets[i].image_number)
            self.enermy_pet_images.append(pet_image)
            self.enermy_pet_images[i].update((self.enermy_image_startx+i*self.pet_width, self.enermy_image_starty))
            enermy_hp_bar = BarImage(self.screen, self.pet_width, self.bar_height, (255, 0, 0),
                                     (255, 255, 255), "HP", 22, self.enermy_pets[i].pet_hp, self.enermy_pets[i].pet_hp)
            enermy_hp_bar.update(self.enermy_pets[i].get_hp(),
                                 (self.enermy_bar_startx + i * self.pet_width, self.enermy_bar_starty))
            self.enermy_hp_bars.append(enermy_hp_bar)

        for i in range(len(self.friend_pets)):
            pet_image = PetImage(self.screen, self.friend_pets[i].pet_file, self.friend_pets[i].image_number)
            self.friend_pet_images.append(pet_image)
            self.friend_pet_images[i].update((self.friend_image_startx-i*self.pet_width, self.friend_image_starty))

        for i in range(len(self.button_images)):
            self.button_images[i].update((self.button_image_startx + i // 3 * self.button_width,
                                          self.button_image_starty + i % 3 * self.button_height))
        self.hp_bar.update(self.player.hp, (5, self.button_image_starty - self.bar_height))
        self.mp_bar.update(self.player.mp, (405, self.button_image_starty - self.bar_height))

    def draw_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        for friend_pet in self.friend_pet_images:
            friend_pet.draw()
        for enermy_pet in self.enermy_pet_images:
            enermy_pet.draw()
        for button in self.button_images:
            button.draw()
        for enermy_hp_bar in self.enermy_hp_bars:
            enermy_hp_bar.draw()

        self.hp_bar.draw()
        self.mp_bar.draw()

    def click_button(self):
        if self.battle_region != None and self.battle_state == BattleState.SelectAction:
            self.button_images[self.battle_region].click()

    def release_button(self):
        if self.battle_region != None:
            self.button_images[self.battle_region].release()

    def friend_attack(self):
        initial_time = time.time()
        current_time = time.time()
        move = 0
        last_time = current_time
        current_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            move += (current_time - last_time) * 50
            if move > 20:
                break
            self.update_screen()
            if self.skill_type == SkillType.NormalAttack or self.skill_type == SkillType.DirectDamage:
                self.enermy_pet_images[self.select_enermy].update((self.enermy_image_startx + self.select_enermy * self.pet_width, self.enermy_image_starty - move))
            elif self.skill_type == SkillType.AreaDamage:
                for i in range(len(self.enermy_pet_images)):
                    self.enermy_pet_images[i].update((self.enermy_image_startx + i * self.pet_width, self.enermy_image_starty - move))
            self.draw_screen()
            pygame.display.flip()
            last_time = current_time
            current_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            move -= (current_time - last_time) * 80
            if move < 0:
                break
            self.update_screen()
            if self.skill_type == SkillType.NormalAttack or self.skill_type == SkillType.DirectDamage:
                self.enermy_pet_images[self.select_enermy].update((self.enermy_image_startx + self.select_enermy * self.pet_width, self.enermy_image_starty - move))
            elif self.skill_type == SkillType.AreaDamage:
                for i in range(len(self.enermy_pet_images)):
                    self.enermy_pet_images[i].update((self.enermy_image_startx + i * self.pet_width, self.enermy_image_starty - move))
            self.draw_screen()
            pygame.display.flip()
            last_time = current_time
            current_time = time.time()
        while current_time - initial_time < 0.8:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.update_screen()
            self.draw_screen()
            pygame.display.flip()
            last_time = current_time
            current_time = time.time()

    def enermy_attack(self, enermy_index):
        initial_time = time.time()
        current_time = time.time()
        move = 0
        last_time = current_time
        current_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            move += (current_time - last_time) * 300
            if move > 100:
                break
            self.update_screen()
            self.enermy_pet_images[enermy_index].update((self.enermy_image_startx + enermy_index * self.pet_width, self.enermy_image_starty + move))
            self.draw_screen()
            pygame.display.flip()
            last_time = current_time
            current_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            move -= (current_time - last_time) * 400
            if move < 0:
                break
            self.update_screen()
            self.enermy_pet_images[enermy_index].update((self.enermy_image_startx + enermy_index * self.pet_width, self.enermy_image_starty + move))
            self.draw_screen()
            pygame.display.flip()
            last_time = current_time
            current_time = time.time()
        while current_time - initial_time < 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.update_screen()
            self.draw_screen()
            pygame.display.flip()
            last_time = current_time
            current_time = time.time()


