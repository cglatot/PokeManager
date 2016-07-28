FROM jfloff/alpine-python:2.7-onbuild

# to build this image, run:
#  docker build --rm=true -t jfloff/app .

# to run this: 
# docker run --rm -it -e "LOGIN=yourlogin@gmail.com" -e "PASSWORD=your-password" -e "STARTINGPOINT=Burlington, VT" ryebrye/pokemongo-manager:latest
                                        
ENV authtype google
ENV WORKING_DIR /usr/local/app                   

COPY . $WORKING_DIR          

# for a flask server    
CMD /bin/bash -c "cd $WORKING_DIR && python pogo/demo.py -a $authtype -u $LOGIN -p $PASSWORD -l '$STARTINGPOINT'" 