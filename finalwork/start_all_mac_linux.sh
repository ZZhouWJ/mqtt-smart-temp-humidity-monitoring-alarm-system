#!/bin/bash
# 推荐：Docker 一键启动整个系统
# chmod +x start_all_mac_linux.sh && ./start_all_mac_linux.sh

docker compose up -d --build

echo "系统已启动："
echo "前端：http://localhost:5173"
echo "后端：http://localhost:8080/api/health"
echo "EMQX：http://localhost:18083 账号 admin 密码 public"
