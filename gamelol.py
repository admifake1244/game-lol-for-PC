import pygame
import random
import sys

# Khởi tạo Pygame
pygame.init()

# Cấu hình các hằng số
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
BIRD_JUMP = -6
PIPE_SPEED = 3
PIPE_GAP = 160

# Màu sắc nâng cấp
COLOR_SKY = (113, 197, 207)
COLOR_BIRD_BODY = (247, 182, 44)
COLOR_BIRD_EYE = (255, 255, 255)
COLOR_BIRD_BEAK = (247, 91, 44)
COLOR_PIPE_MAIN = (115, 191, 46)
COLOR_PIPE_DARK = (82, 126, 31)
COLOR_GROUND = (222, 216, 149)
COLOR_GRASS = (155, 210, 114)
WHITE = (255, 255, 255)

# Khởi tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Pro Edition by admifake1244")
clock = pygame.time.Clock()
font_score = pygame.font.SysFont("Arial", 40, bold=True)
font_msg = pygame.font.SysFont("Arial", 24, bold=True)

def draw_bird(screen, rect, movement):
    """Vẽ chú chim chi tiết hơn với mắt và mỏ"""
    # Xoay chim dựa trên chuyển động
    rotation = -movement * 3
    bird_surface = pygame.Surface((44, 34), pygame.SRCALPHA)
    
    # Thân chim (Hình oval)
    pygame.draw.ellipse(bird_surface, COLOR_BIRD_BODY, (0, 0, 34, 24))
    pygame.draw.ellipse(bird_surface, (0, 0, 0), (0, 0, 34, 24), 2)
    
    # Cánh
    pygame.draw.ellipse(bird_surface, WHITE, (5, 8, 15, 10))
    pygame.draw.ellipse(bird_surface, (0, 0, 0), (5, 8, 15, 10), 1)
    
    # Mắt
    pygame.draw.circle(bird_surface, WHITE, (25, 8), 5)
    pygame.draw.circle(bird_surface, (0, 0, 0), (27, 8), 2)
    
    # Mỏ
    pygame.draw.polygon(bird_surface, COLOR_BIRD_BEAK, [(32, 10), (42, 15), (32, 20)])
    pygame.draw.polygon(bird_surface, (0, 0, 0), [(32, 10), (42, 15), (32, 20)], 1)
    
    rotated_bird = pygame.transform.rotate(bird_surface, rotation)
    screen.blit(rotated_bird, rotated_bird.get_rect(center=rect.center))

def draw_pipe(screen, pipe_list):
    """Vẽ ống với nắp và đổ bóng chuyên nghiệp"""
    for pipe in pipe_list:
        rect = pipe["rect"]
        # Thân ống
        pygame.draw.rect(screen, COLOR_PIPE_MAIN, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        
        # Đổ bóng cho thân ống (vạch dọc)
        shadow_rect = pygame.Rect(rect.left + 5, rect.top, 10, rect.height)
        pygame.draw.rect(screen, (140, 215, 70), shadow_rect)
        
        # Vẽ nắp ống
        if rect.bottom >= SCREEN_HEIGHT: # Ống dưới
            head_rect = pygame.Rect(rect.left - 5, rect.top, rect.width + 10, 30)
        else: # Ống trên
            head_rect = pygame.Rect(rect.left - 5, rect.bottom - 30, rect.width + 10, 30)
            
        pygame.draw.rect(screen, COLOR_PIPE_MAIN, head_rect)
        pygame.draw.rect(screen, (0, 0, 0), head_rect, 2)

def draw_clouds(clouds):
    """Vẽ các đám mây trang trí"""
    for cloud in clouds:
        pygame.draw.circle(screen, WHITE, (cloud[0], cloud[1]), 20)
        pygame.draw.circle(screen, WHITE, (cloud[0] + 15, cloud[1] - 5), 25)
        pygame.draw.circle(screen, WHITE, (cloud[0] + 30, cloud[1]), 20)

def main():
    bird_rect = pygame.Rect(50, SCREEN_HEIGHT // 2, 34, 24)
    bird_movement = 0
    
    pipe_list = []
    clouds = [[random.randint(0, SCREEN_WIDTH), random.randint(50, 200)] for _ in range(5)]
    
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1400)
    
    score = 0
    high_score = 0
    game_active = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird_movement = BIRD_JUMP
                    else:
                        game_active = True
                        pipe_list.clear()
                        bird_rect.center = (50, SCREEN_HEIGHT // 2)
                        bird_movement = 0
                        score = 0
            
            if event.type == SPAWNPIPE and game_active:
                random_pos = random.randint(200, 450)
                bottom_p = pygame.Rect(SCREEN_WIDTH, random_pos, 60, SCREEN_HEIGHT)
                top_p = pygame.Rect(SCREEN_WIDTH, random_pos - PIPE_GAP - 500, 60, 500)
                pipe_list.append({"rect": bottom_p, "passed": False})
                pipe_list.append({"rect": top_p, "passed": False})

        # Cập nhật logic
        if game_active:
            bird_movement += GRAVITY
            bird_rect.centery += bird_movement
            
            # Di chuyển ống
            for pipe in pipe_list:
                pipe["rect"].centerx -= PIPE_SPEED
            pipe_list = [p for p in pipe_list if p["rect"].right > -50]
            
            # Di chuyển mây
            for cloud in clouds:
                cloud[0] -= 0.5
                if cloud[0] < -60: cloud[0] = SCREEN_WIDTH + 20
            
            # Kiểm tra va chạm
            for pipe in pipe_list:
                if bird_rect.colliderect(pipe["rect"]): game_active = False
            if bird_rect.top <= 0 or bird_rect.bottom >= 550: game_active = False
            
            # Tính điểm
            for pipe in pipe_list:
                if pipe["rect"].right < bird_rect.left and not pipe["passed"]:
                    pipe["passed"] = True
                    score += 0.5
        
        # Vẽ màn hình
        screen.fill(COLOR_SKY)
        
        # Vẽ mây
        draw_clouds(clouds)
        
        # Vẽ ống
        draw_pipe(screen, pipe_list)
        
        # Vẽ mặt đất
        pygame.draw.rect(screen, COLOR_GROUND, (0, 550, SCREEN_WIDTH, 50))
        pygame.draw.rect(screen, COLOR_GRASS, (0, 550, SCREEN_WIDTH, 15))
        pygame.draw.line(screen, (0, 0, 0), (0, 550), (SCREEN_WIDTH, 550), 2)
        
        if game_active:
            draw_bird(screen, bird_rect, bird_movement)
            # Hiển thị điểm phong cách Flappy
            score_surf = font_score.render(str(int(score)), True, WHITE)
            score_rect = score_surf.get_rect(center=(SCREEN_WIDTH//2, 80))
            # Vẽ bóng cho chữ
            shadow_surf = font_score.render(str(int(score)), True, (50, 50, 50))
            screen.blit(shadow_surf, (score_rect.x+2, score_rect.y+2))
            screen.blit(score_surf, score_rect)
        else:
            if score > high_score: high_score = score
            # Màn hình kết thúc nâng cấp
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (0,0))
            
            msg = font_score.render("GAME OVER", True, (255, 255, 255))
            screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH//2, 200)))
            
            s_msg = font_msg.render(f"SCORE: {int(score)}  |  BEST: {int(high_score)}", True, COLOR_BIRD_BODY)
            screen.blit(s_msg, s_msg.get_rect(center=(SCREEN_WIDTH//2, 260)))
            
            r_msg = font_msg.render("Press SPACE to Restart", True, WHITE)
            screen.blit(r_msg, r_msg.get_rect(center=(SCREEN_WIDTH//2, 350)))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()