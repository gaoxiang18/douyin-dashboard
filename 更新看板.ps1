# 抖音电商数据看板 - 一键更新脚本
# 使用方法：双击运行或右键"使用PowerShell运行"

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 切换到看板目录
Set-Location "d:\mydata\桌面\skill\douyin-dashboard"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  抖音电商数据看板 - 数据更新工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否有更改
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "✓ 没有需要更新的更改" -ForegroundColor Green
    Write-Host ""
    pause
    exit
}

# 显示更改的文件
Write-Host "检测到以下更改：" -ForegroundColor Yellow
git status --short
Write-Host ""

# 添加所有更改
git add .

# 获取提交信息
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMsg = "数据更新 $timestamp"

# 提交
git commit -m $commitMsg

# 推送
Write-Host ""
Write-Host "正在推送到GitHub..." -ForegroundColor Cyan
git push

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✓ 更新成功！" -ForegroundColor Green
Write-Host "  访问链接: https://gaoxiang18.github.io/douyin-dashboard/" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "提示：GitHub Pages 需要1-2分钟同步更新" -ForegroundColor Gray
Write-Host ""
pause
