from os import walk
import pygame

def import_folder(path):
    surface_list = []

    print("import folder",path)
    for _,__,image_files in walk(path):
        print("walking")
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
            print("loaded", full_path)

    return surface_list