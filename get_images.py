import docker
import json
from termcolor import colored

def remove_char(line,chars):
    return line.translate(None,chars)

def get_images(images):
    images_and_tags_list = {}
    for image in images:
        str_image = str(image)
        if ('registry.mindklab.com:5000' not in str_image)or( '<Image:' not in str_image):
            str_image_tags = str(image.tags)
            str_images_tags_splited = str_image_tags.split(" ")
            for image_tag in str_images_tags_splited:
                if image_tag != '<Image:':
                    image_tag = remove_char(image_tag,",'<>[]")
                    image_tag = image_tag[1:]
                    tags_list = []
                    image, tag = image_tag.split(":")
                    #				print "image: " + image
                    #				print "tag:" + tag
                    if (tag != 'latest') and (tag != 'local'):
                        if image in images_and_tags_list.keys():
                            tags_list = images_and_tags_list[image]
                        tags_list.append(tag)
                        images_and_tags_list[image] = tags_list
    return images_and_tags_list

def sort_tag(images_and_tags_list ):
    print "sorting " + str(images_and_tags_list) + "\n"
    for key, values in images_and_tags_list.items():
        values = sorted(values)
        tags_count = len(values)
        current_tag = 0
        for value in values:
            output_color = 'green'
            if (tags_count != 1)and(current_tag +1) != tags_count:
                output_color = 'red'
            print  colored ( str(key)+ ":" + str(value),output_color)
            current_tag += 1


def main():
    client = docker.from_env()
    images = client.images.list()
    images_and_tags_list = get_images(images)
    sorted_images_and_tags_list = sort_tag(images_and_tags_list )


'''
	#to output in json format: 
	print " " 
	print json.dumps(images_and_tags_list, indent=2)
	print " "
#'''

if __name__ == "__main__":
    main()
