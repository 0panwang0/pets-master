import pygame
screen_size = (800, 600)

shop_file_name =  "resources/images/shop.tga"
icon_file_name = "resources/images/IconSet.png"
arrow_file_name = "resources/images/arrow.png"
font_file_name = "resources/fonts/ink.ttf"


item_dict = { '萝卜':(0, 18), '洋葱':(1, 18), '土豆':(2, 18), '生肉':(3, 18), '鲜鱼':(4, 18),}

class Shop:
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.large_font = pygame.font.Font(font_file_name, 40)
        self.small_font = pygame.font.Font(font_file_name, 20)
        self.icon = pygame.image.load(icon_file_name).convert()
        self.arrow = pygame.image.load(arrow_file_name).convert_alpha()
        self.shop = pygame.image.load(shop_file_name).convert_alpha()
        self.shop_item = ["萝卜", "洋葱", "土豆", "生肉", "鲜鱼"]
        self.state = 0
        self.item_introduce = {
            "萝卜":"十字花科萝卜属植物",
            "洋葱":"百合科葱属植物",
            "土豆":"茄科茄属植物",
            "生肉":"富含蛋白质的生肉",
            "鲜鱼":"富含维生素的鲜鱼"
        }
        self.item_change = {
            "萝卜": "生命值+100，金币-20",
            "洋葱": "法力值+100，金币-20",
            "土豆": "生命值+50，法力值+50，金币-20",
            "生肉": "最大生命值+10，金币-20",
            "鲜鱼": "最大法力值+10，金币-20"
        }
        self.item_price = {
            "萝卜": 20,
            "洋葱": 30,
            "土豆": 25,
            "生肉": 20,
            "鲜鱼": 10
        }

    def draw(self):
        self.player.controller = "shop"
        self.shop = pygame.image.load(shop_file_name).convert_alpha()
        self.shop.blit(self.large_font.render('商店', True, (0, 0, 0)), (170, 50))
        self.draw_arrow()
        for i in range(len(self.shop_item)):
            self.shop.blit(self.get_image(item_dict[self.shop_item[i]]), (20, 120+i*30))
        if self.state == 0:
            self.draw_introduce()
        elif self.state == 1:
            self.draw_change()
        self.screen.blit(self.shop, ((screen_size[0]-self.shop.get_width())/2, (screen_size[1]-self.shop.get_height())/2,))
        pygame.display.update()
        self.take_control()

    def draw_introduce(self):
        for i in range(len(self.shop_item)):
            self.shop.blit(self.small_font.render(self.shop_item[i]+"："+self.item_introduce[self.shop_item[i]], True, (0, 0, 0)), (50, 120+i*30))

    def draw_change(self):
        for i in range(len(self.shop_item)):
            self.shop.blit(self.small_font.render(self.shop_item[i] + "：" + self.item_change[self.shop_item[i]], True, (0, 0, 0)), (50, 120 + i * 30))

    def draw_arrow(self):
        self.shop.blit(self.arrow, (320, 280))

    def get_image(self, pos):
        return self.icon.subsurface(24 * pos[0], 24 * pos[1], 24, 24)

    def take_control(self):
        while self.player.controller != 'main':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE):
                    self.player.controller = 'main'
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and pygame.Rect(
                    320 + (screen_size[0] - self.shop.get_width()) / 2,
                    280 + (screen_size[1] - self.shop.get_height()) / 2, self.arrow.get_width(),
                    self.arrow.get_height()).collidepoint(pygame.mouse.get_pos()):
                    self.state = (self.state + 1) % 2
                    self.draw()


