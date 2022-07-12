
# 还不太清楚哪个命令没有-y这种的，还得手动输入 y 才能让程序运行

# [docker]
# 移除旧的docker
yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
# 配置阿里云的 docker 仓库
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
dnf -y install https://mirrors.aliyun.com/docker-ce/linux/centos/7/x86_64/stable/Packages/containerd.io-1.2.13-3.1.el7.x86_64.rpm
dnf -y install docker-ce
# 下载docker-ce的repo
curl https://download.docker.com/linux/centos/docker-ce.repo -o /etc/yum.repos.d/docker-ce.repo
dnf -y  install docker-ce  docker-ce-cli --nobest
# 启动docker
systemctl start docker

docker -v
# 自启动docker
systemctl enable --now docker

yum -y install screen htop



