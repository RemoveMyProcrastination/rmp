FROM python:3.5
MAINTAINER akash

# python 3.5 works off debian jessie, so we follow jessie
# related instructions to install couchdb.

# from https://cwiki.apache.org/confluence/display/COUCHDB/Debian

# Ommitted as suggested by http://jeeonthepi.blogspot.com/2014/08/installing-couchdb-1.html
#RUN apt-get update && apt-get install -y lsb-release
#RUN echo "deb http://binaries.erlang-solutions.com/debian `lsb_release -cs` contrib" \
#  | tee /etc/apt/sources.list.d/erlang-solutions.list
#RUN wget -O - http://binaries.erlang-solutions.com/debian/erlang_solutions.asc \
#  | apt-key add -
#RUN apt-get update -y
#RUN apt-get install -y libmozjs185-1.0 libmozjs185-dev

# Instead, we do this:
# update repository cache
RUN apt-get update &&  apt-get install -y \
  libmozjs185-1.0 \
  libmozjs185-dev


RUN apt-get install -y erlang-nox erlang-dev
RUN apt-get install -y build-essential

RUN apt-get install -y libnspr4 libnspr4-0d libnspr4-dev libcurl4-openssl-dev curl libicu-dev
RUN useradd -d /var/lib/couchdb couchdb
RUN mkdir -p /usr/local/{lib,etc}/couchdb /usr/local/var/{lib,log,run}/couchdb /var/lib/couchdb
RUN chown -R couchdb:couchdb /usr/local/{lib,etc}/couchdb /usr/local/var/{lib,log,run}/couchdb
RUN chmod -R g+rw /usr/local/{lib,etc}/couchdb /usr/local/var/{lib,log,run}/couchdb

# this line is different from directions -- it says download the file, so we use wget to do that
RUN wget http://apache.mirrors.tds.net/couchdb/source/1.6.1/apache-couchdb-1.6.1.tar.gz -O apache-couchdb.tar.gz

RUN tar xzf apache-couchdb.tar.gz

RUN cd apache-couchdb-* \
 &&  ./configure --prefix=/usr/local --with-js-lib=/usr/lib --with-js-include=/usr/include/mozjs --enable-init \
 && make && make install

<<<<<<< HEAD
# Finally, install flask.

RUN pip install \
  flask \
  couchdb

VOLUME /var/flask

COPY ./start.sh /
=======
# Finally, install python stuff.

RUN pip install --upgrade pip && pip install \
  flask \
  couchdb \
  bcrypt

VOLUME /var/flask

COPY docker_setup/start.sh /
>>>>>>> dd4129b88d5a096b478020d24c572470740a2b7a

WORKDIR /var/flask

CMD ["/start.sh"]
  


