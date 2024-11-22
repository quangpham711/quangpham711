import pygame
import random

def background_with_stars(screen, num_stars=100):
    """
    Hiệu ứng nền với các ngôi sao di chuyển theo chuột và tạo hiệu ứng nhòe.

    Args:
        screen (pygame.Surface): Màn hình để vẽ hiệu ứng nền.
        num_stars (int): Số lượng ngôi sao trên nền.
    """
    # Kích thước màn hình
    screen_width, screen_height = screen.get_size()

    # Tạo danh sách các ngôi sao
    stars = [{"x": random.randint(0, screen_width), 
              "y": random.randint(0, screen_height), 
              "speed": random.uniform(1, 4)} for _ in range(num_stars)]

    # Màu sắc
    black = (0, 0, 0)
    white = (255, 255, 255)
    fade_color = (5, 5, 5)  # Màu làm tối nền (hiệu ứng nhòe)

    # Biến lưu vị trí chuột trước đó
    prev_mouse_pos = pygame.mouse.get_pos()

    clock = pygame.time.Clock()

    # Hiển thị con trỏ
    pygame.mouse.set_visible(True)


    # Lấy vị trí chuột hiện tại
    mouse_pos = pygame.mouse.get_pos()
    dx = prev_mouse_pos[0] - mouse_pos[0]
    dy = prev_mouse_pos[1] - mouse_pos[1]

        # Tạo hiệu ứng nhòe bằng cách làm tối nền thay vì xóa toàn bộ
    dark_surface = pygame.Surface((screen_width, screen_height))
    dark_surface.set_alpha(80)  # Điều chỉnh độ trong suốt của lớp tối
    dark_surface.fill(fade_color)
    screen.blit(dark_surface, (0, 0))
    
    # Cập nhật vị trí các ngôi sao
    for star in stars:
        star["x"] += dx * star["speed"] * 0.3  # Di chuyển nhanh hơn
        star["y"] += dy * star["speed"] * 0.3

        # Nếu ngôi sao ra khỏi màn hình, đưa ngôi sao trở lại màn hình
        if star["x"] < 0:
            star["x"] += screen_width
        elif star["x"] > screen_width:
            star["x"] -= screen_width
        if star["y"] < 0:
            star["y"] += screen_height
        elif star["y"] > screen_height:
            star["y"] -= screen_height

    # Vẽ các ngôi sao
    for star in stars:
        pygame.draw.circle(screen, white, (int(star["x"]), int(star["y"])), 2)

        # Cập nhật màn hình
        pygame.display.flip()

        # Lưu vị trí chuột trước đó
        prev_mouse_pos = mouse_pos

        # Điều chỉnh tốc độ khung hình
        clock.tick(60)
