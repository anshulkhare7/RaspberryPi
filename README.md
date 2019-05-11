## Steps to Setup Raspberry Pi (In headless mode)

1. Using Balena Etcher, burn the image [2019-04-08-raspbian-stretch-full.zip](http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-04-09/2019-04-08-raspbian-stretch.zip) to micro sd card.
2. In the freshly created boot drive, create an empty file named `ssh` in the boot folder. This is for enabling ssh access by default.
    - In linux, mount the sd card `sudo mkdir /media/sdcard && sudo mount /dev/sdb1 /media/sdcard`
3. Create another file called [wpa_supplicant.conf](https://gist.github.com/anshulkhare7/fdd662c358a2ff7eba48fd11050b9243). This is for enabling wifi and configuring default wifi connection details.
4. Power on Raspberry with the sd card. 
5. Figure out the IP address of Raspberry. 
    - From the Wifi Admin console. Or,
    - Using network scanning tool like **nmap** — `nmap -sP 192.168.x.0/24`    
6. SSH to raspi with default credentials, i.e., **login: pi** and **password: raspberry**
7. Install Dataplicity.
8. Change password with command `passwd`
9. Free up space by uninstalling following libraries.<br>
  `sudo apt-get purge -y wolfram-engine libreoffice* && sudo apt-get clean && sudo apt-get autoremove -y`
10. Expand the file system `sudo raspi-config`
    > Advance Options —> Expand File Systems
    > Reboot
11. Update and upgrade `sudo apt-get update -y && sudo apt-get upgrade -y`
12. Install Vim `sudo apt-get install vim`
13. Install PIP
    - `wget https://bootstrap.pypa.io/get-pip.py`
    - `sudo python3 get-pip.py`
    - `sudo rm -rf ~/get-pip.py ~/.cache/pip`
14. Install pre requisites for Open CV3
    - `sudo apt-get install -y libhdf5-dev libhdf5-serial-dev libhdf5-100`
    - `sudo apt-get install -y libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5`
    - `sudo apt-get install -y libatlas-base-dev`
    - `sudo apt-get install -y libjasper-dev`
    - `sudo apt-get install -y build-essential cmake pkg-config`
    - `sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev`
    - `sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev`
    - `sudo apt-get install -y libxvidcore-dev libx264-dev`
    - `sudo apt-get install -y libgtk2.0-dev libgtk-3-dev`
    - `sudo apt-get install -y libatlas-base-dev gfortran`
    - `sudo apt-get install -y python2.7-dev python3-dev`
    - `sudo apt-get install ffmpeg -y`
    - `sudo apt-get install byobu -y` 
15. Install Virtual Environment
    - `pip install virtualenv=='16.6.1' virtualenvwrapper=='4.8.4' --user`
    - `echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile`
    - `echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile`
    - `echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.profile`
    - `echo "source /home/pi/.local/bin/virtualenvwrapper.sh" >> ~/.profile`
    - Add /home/pi/.local/bin/ to $PATH (in ~/.profile)
    - `source ~/.profile`
    - `mkvirtualenv cv3-py2 -p python2`
16. Use byobu for running detached ssh sessions. So that, even if dataplicity gets disconnected, your installation process isn't interrupted.
17. Activate virtual env and install Numpy
    - `workon cv3-py2`
    - `pip install numpy=='1.16.4'`
18. Install OpenCV3 by compiling. [Source](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)
    - `cd ~ && wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.3.0.zip`
    - `unzip opencv.zip`
    - `wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.3.0.zip`
    - `unzip opencv_contrib.zip`
    - `mkdir ~/opencv-3.3.0/build && cd ~/opencv-3.3.0/build`
    - `cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_FFMPEG=ON -D WITH_TBB=ON -D WITH_GTK=ON -D WITH_V4L=ON -D WITH_OPENGL=ON -D WITH_CUBLAS=ON -DWITH_QT=OFF -DCUDA_NVCC_FLAGS="-D_FORCE_INLINES" -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules -D BUILD_EXAMPLES=ON ..`
    - Increase swap size
      - `sudo vim /etc/dphys-swapfile`
      - Update CONF_SWAPSIZE=1024
      - `sudo /etc/init.d/dphys-swapfile stop`
      - `sudo /etc/init.d/dphys-swapfile start`
    - `make -j4`
    - `sudo make install`
    - `sudo ldconfig`
    - `cd ~/.virtualenvs/cv3-py2/lib/python2.7/site-packages/`
    - `ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so`
19. Installing Keras and Tensorflow. [Source](https://www.pyimagesearch.com/2017/12/18/keras-deep-learning-raspberry-pi/)
    - `wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.1.0/tensorflow-1.1.0-cp27-none-linux_armv7l.whl`
    - `pip install tensorflow-1.1.0-cp27-none-linux_armv7l.whl`
    - `sudo apt-get install libhdf5-serial-dev`
    - `pip install h5py`
    - `pip install pillow imutils`
    - `pip install scipy --no-cache-dir`
    - `pip install keras==2.1.5`
20. Revert swap size
    - `sudo vim /etc/dphys-swapfile`
    - Update CONF_SWAPSIZE=100
    - `sudo /etc/init.d/dphys-swapfile stop`
    - `sudo /etc/init.d/dphys-swapfile start`
21. Install Nginx
    - `sudo apt install -y nginx`
    - Setup basic authentication `echo “innocule: 'openssl passwd -apr1'" | sudo tee -a /etc/nginx/htpasswd.users`
    - Check nginx config `sudo nginx -t`
    - Restart nginx `sudo systemctl nginx restart`
22. Clone the github repo. `git clone git@github.com:<github-repo>`
23. Add crontab for restarting the flask process on reboot.
    - `crontab -e`
    - Add this to crontab — `@reboot <path to startup script>/startflask.sh`
24. Create a [backup image of SD card](https://www.youtube.com/watch?v=sUYVKhI_84E)
    - Connect the SD card to laptop and check the name `lsblk` and space `df -h`
    - Unmount the SD card, E.g. `— sudo umount /dev/sdb1 && sudo umount /dev/sdb2`
    - Create a img file `sudo dd if=/dev/sdb of=backup-image.img bs=4M; sync`
    
