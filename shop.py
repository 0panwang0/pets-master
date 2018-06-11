import pygame
screen_size = (800, 600)

shop_file_name =  "resources/images/shop.tga"
icon_file_name = "resources/images/IconSet.png"
font_file_name = "resources/fonts/ink.ttf"

item_dict = { '萝卜':(0, 18), '洋葱':(1, 18), '土豆':(2, 18), '生肉':(3, 18), '鲜鱼':(4, 18),}

class Shop:
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.large_font = pygame.font.Font(font_file_name, 40)
        self.small_font = pygame.font.Font(font_file_name, 20)
        self.icon = pygame.image.load(icon_file_name).convert()
        self.shop = pygame.image.load(shop_file_name).convert_alpha()
        self.shop_item = ["萝卜", "洋葱", "土豆", "生肉", "鲜鱼"]
        self.item_introduce = {
            "萝卜":"红棕色棒状物体",
            "洋葱":"里面充满褶皱的淡红色物体",
            "土豆":"又黑又粗",
            "生肉":"不是熟的",
            "鲜鱼":"带震动的了解一下"
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
        self.draw_item()
        self.screen.blit(self.shop, ((screen_size[0]-self.shop.get_width())/2, (screen_size[1]-self.shop.get_height())/2,))
        pygame.display.update()
        self.take_control()

    def draw_item(self):
        for i in range(len(self.shop_item)):
            self.shop.blit(self.get_image(item_dict[self.shop_item[i]]), (20, 120+i*30))
            self.shop.blit(self.small_font.render(self.shop_item[i]+"："+self.item_introduce[self.shop_item[i]], True, (0, 0, 0)), (60, 120+i*30))

    def get_image(self, pos):
        return self.icon.subsurface(24 * pos[0], 24 * pos[1], 24, 24)

    def take_control(self):
        while self.player.controller != 'main':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.controller = 'main'

