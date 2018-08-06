import docker
import json
from termcolor import colored

def remove_char(line,chars):
    return line.translate(None,chars)

def get_images(images):
    images_and_tags_list = {}
    for image in images:
        str_image = str(image)
        if ('registry.mindklab.com:5000' not in str_image):
            if( "<Image: ''>" not in str_image):
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

def print_old_tags(tag_number_list):
    print "We need to delete next images:"
    for images, tags in tag_number_list.items():
        for tag_name, tag_number in tags.items():
            tag_number = sorted(tag_number)
            len_tag_number = len(tag_number)
            if len_tag_number > 1:
#                print images + " : " + str(tag_name) + " . " + str(tag_number)
                current_tag_count = 0
                for tag in tag_number:
                    current_tag_count +=1
                    if current_tag_count != len_tag_number:
                        print images + ":" + str(tag_name) + "." + str(tag)



def sort_tag(images_and_tags_list ):
#    print "sorting " + str(images_and_tags_list) + "\n"
    images_tags_number_list = {}
    for key, values in images_and_tags_list.items():
        values = sorted(values)
        tags_count = len(values)
        current_tag = 0
        tag_name_list = {}
        tag_number_list = []
        current_value = ''
        prev_value = ''
        for value in values:

            output_color = 'green'
            if (tags_count != 1)and(current_tag +1) != tags_count:
                output_color = 'red'
#            print  colored ( str(key)+ ":" + str(value),output_color)
            current_tag += 1
            dot_position = str(value).rfind('.')
            if dot_position != -1:
                tag_name = str(value)[:dot_position]
                tag_number = str(value)[dot_position+1:]
                current_value = tag_name
                if prev_value != current_value:
                    prev_value = current_value
                    tag_number_list = []
                tag_number_list.append(tag_number)
                tag_name_list[tag_name] = (tag_number_list)
                images_tags_number_list[key] = tag_name_list
#                print colored(str(key), 'blue') + " : " +colored(tag_name,'red') + " . " + colored(tag_number,'green')
#                  if str(key) == 'sfreydin/test_image_1':
#                      print tag_number_list
    print_old_tags(images_tags_number_list)

    return images_tags_number_list

def print_list():
    client = docker.from_env()
    images = client.images.list()
    images_and_tags_list = get_images(images)
    sorted_images_and_tags_list = sort_tag(images_and_tags_list )


'''
	#to output in json format: 
	print " " 
	print json.dumps(images_and_tags_list, indent=2)
	print json.dumps(sorted_images_and_tags_list, indent=2)
	print " "
#'''

if __name__ == "__main__":
    print_list()
