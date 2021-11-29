# git使用教程

**分布式和集中式有何不同？**：首先，分布式版本控制系统根本没有“中央服务器”，每个人的电脑上都是一个完整的版本库，这样，你工作的时候，就不需要联网了，因为版本库就在你自己的电脑上。既然每个人电脑上都有一个完整的版本库，那多个人如何协作呢？比方说你在自己电脑上改了文件A，你的同事也在他的电脑上改了文件A，这时，你们俩之间只需把各自的修改推送给对方，就可以互相看到对方的修改了。

和集中式版本控制系统相比，分布式版本控制系统的安全性要高很多，因为每个人电脑里都有完整的版本库，某一个人的电脑坏掉了不要紧，随便从其他人那里复制一个就可以了。而集中式版本控制系统的中央服务器要是出了问题，所有人都没法干活了。

在实际使用分布式版本控制系统的时候，其实很少在两人之间的电脑上推送版本库的修改，因为可能你们俩不在一个局域网内，两台电脑互相访问不了，也可能今天你的同事病了，他的电脑压根没有开机。因此，分布式版本控制系统通常也有一台充当“中央服务器”的电脑，但这个服务器的作用仅仅是用来方便“交换”大家的修改，没有它大家也一样干活，只是交换修改不方便而已。

## 配置

```shell
# 配置Git仓库的用户名和邮箱，全局生效
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
# 配置Git仓库代理
git config --global http.proxy http://127.0..0.1:8080
git config --global https.proxy https://127.0.0.1:8080
# 取消配置项
git config --global --unseu [配置名称]
git config --list 	# 查看当前git的配置
# 创建一个版本库，使用gitbash操作
mkdir learngit
cd learngit
git init	# 这一步是把这个目录变成Git可以管理的仓库，创建好后，目录下多了个.git隐藏目录，这个隐藏目录是用来跟踪管理版本库的。
```

## 文件操作

`HEAD`在Git中，他是一个指向你正在工作的本地分支的指针，可以将`HEAD`想象为当前分支的别名。

### 提交文件

```shell
# 将修改过的readme.txt文件添加到暂存区
git add readme.txt		# 先添加到本地版本库，也可以用git add *把当前目录下所有内容添加
# 把暂存区的所有内容提交到当前分支
git commit -m "wrote a readme file"		# -m 后面输入的是本次提交的说明，可以输入任意内容，当然是有意义的最好，这样就能从历史记录里方便地找到改动记录。

```

### 查看文件修改情况

```shell
git diff FileName 	# 查看文件是否被修改，如果修改则和上一次保存的文件进行比对，查看更改了哪些内容
git diff HEAD -- readme.md		# 查看工作区和版本库里面最新版本的区别
git status			# 查询当前仓库的状态，可以查询哪些文件已经被修改，但还没有准备提交的修改。
```

### 撤销修改

```shell
git checkout -- readme.md		# 把readme.txt文件在工作区的修改全部撤销。撤销操作一定要注意添加--，如果没有--，则checkout就相当于切换分支操作。
git reset HEAD <file>			# 把暂存区的修改撤销掉(unstage)，重新放回到工作区。
```

### 删除文件

```shell
# 情况一：确实需要从版本库中删除文件
git rm <file>
git commit -m "remove file"
# 情况二： 删错了，但版本库里还有，所以轻松的把误删的文件恢复到最新版本
git checkout -- readme.md		# git checkout其实使用版本库里的版本替换到工作区的版本，无论工作区是修改还是删除，都可以"一键还原"
```

**注意**：从来没有被添加到版本库就被删除的文件，是无法恢复的；命令`git rm`用于删除一个文件。如果一个文件已经被提交到版本库，那么你永远不用担心误删，但是要小心，你只能恢复文件到最新版本，你会丢失**最近一次提交后你修改的内容**。



### 版本回退

```shell
git log 			# 显示从最近到最远的提交日志
	--pretty=oneline	# 精简版log日志，所有操作一行显示
	
# 当前版本回退到上一个版本
git reset --hard HEAD^	#也可以将HEAD换成commit id的哈希值，这样就可以指定回到未来的某个版本；HEAD~100 表示回退到100个版本之前。也可以指定ID来d
git reflog			# 查看历史命令，以便确定要回到哪个版本
```

### 工作区和暂存区

**工作区**

就是你在电脑里能看到的目录，比如learngit文件夹就是一个工作区；

**版本库**

工作区有一个隐藏目录**.git**，这个不算工作区，而是Git的版本库。

Git的版本库里存了很多东西，其中比较重要的就是称为stage（或者叫index）的暂存区，还有Git为我们自动创建的第一个分支**master**，以及指向master的一个指针交**HEAD**

## 远程仓库

由于本地Git仓库和GitHub仓库之间的传输是通过SSH加密的，所以，需要一点设置：

- `ssh-keygen -t  rsa -C "liuzeming@storswift.com"`
- 登录GitHub，打开"Account settings"， "在SSH Kesys"页面点击"Add SSH Key"，填上任意Title，在Key文本框粘贴`id_rsa。pub`文件的内容

### 使用命令行创建一个新的存储库并合并仓库

```shell
echo "# Python" >> README.md
git init	# 初始化一个本地目录为本地Git仓库
git add README.md
git commit -m "frist commit"
# 移动/重命名一个分支，即使已经目标已经存在
git branch -M main 	
# 添加远程库
git remote add origin https://github.com/liuzeming1/Python.git		# 也可以使用 git remote add origin git@github.com:liuzeming1/Python.git
#添加好远程仓库后，拉去远程仓库，合并到本地
git pull origin main		# 第一次拉去会报错，原因是远程仓库和本地仓库两者历史记录不一样应当使用一下命令
git pull origin main --allow-unrelated-histories
# 将本地仓库commit的内容同步到远程仓库
git push -u origin main		# 加了-u 参数，Git不但会把本地的main分支内容推送到远程的main分支，还会把本地的main分支和远程的main分支关联起来，在以后的推送或者拉起时就可以简化命令。
```

### 删除远程库

```shell
# 如果添加的时候地址写错了，或者就是想删除远程库，可以用git remote rm <name>命令。使用前先用git remote -v查看远程库信息
git remote -v
# 然后根据名字删除，比如删除origin
git remote rm origin
# 此处的“删除”其实是解除了本地与远程的绑定关系，并不是物理上删除了远程库。远程库本身并没有任何改动。想要正在删除远程库，需要登录到GitHub，在后台页面找到删除按钮在删除。
```

## 分支管理

新建分支		`git branch <name>（自定义命名分支）`

创建+切换分支	`git checkout -b <name>`或者`git switch -c <name>`

检查分支是否创建成功	`git branch`	-a：查看远程分支

切换分支		`git checkout <name>`或者`git switch <name>`

合并分支		`git merge <name>`	指定分支合并到当前分支；`--no-ff`合并时禁用`Fast forward`模式，由于默认使用`Fast forward`模式分支信息会丢失，所以用这个参数就可以从分支历史上看到分支信息。

删除本地分支		`git branch -d <name>`

删除远程分支 `git push origin -d <分支名>`

查看远程仓库分支和本地仓库的远程分支记录的对应关系	`git remote show origin`

删除远程仓库已经删除过的分支	`git remote prune origin`	

**新版特性**

创建并切换到新的`dev`分支：

```shell
git switch -c dev
```

直接切换到已有的`master`分支

```shell
git switch master
```

### 解决合并冲突

```shell
# 准备新的feature1分支
$ git switch -c feature1
Switched to a new branch 'feature1'
# 修readme.txt最后一行
Creating a new branch is quck AMD simple.
# 在feature1分支上提交
$ git add README.md
$ git commit -m "AMD simple"
[feature1 56d7e65] AMD simple
 1 file changed, 1 insertion(+)
# 切换到master分支
$ git switch master
# 在master分支上把README.md文件最后一行改为：
Creating a new branch is quck % simple.
# 提交：
$ git add README.md
$ git commit -m "& simple"
[main ec65d17] & simple
 1 file changed, 2 insertions(+)
# 现在这种情况，Git无法完成“快速合并”，只能试图把各自修改的合并起来，但这种合并就可能会有冲突
$ git merge feature1
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
# 使用git status也会告诉我们冲突的文件
$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)
# 直接查看README。md的内容
#learngit
<<<<<<< HEAD
Creating a new branch is quck & simple.

=======
Creating a new branch is quck AMD simple.
>>>>>>> feature1
# Git用<<<<<<<, ========, >>>>>>>标记出不同分支的内容，就可以了；最后删除featu1分支
git branch -d feature1
# 错误处理：fatal: You have not concluded your merge (MERGE_HEAD exists)
# 解决方式一：保留本地的更改，终止合并->重新合并->重新拉取
git merge --abort
git reset --merge
git pull
# 解决方案二： 舍弃本地代码，远端版本覆盖本地版本(慎重)
git fetch --all
git reset --hard origin/master
git fetch
```

`git fetch`和`git pull`的区别：

`git fetch`只是从远程获取最新版本到本地，不会`merge`

`git pull`从远程获取最新版本并`merge`到本地

**小结**

当Git无法自动合并分支时，就必须先解决冲突。解决冲突后，再提交，合并完成。

解决冲突就是把Git合并失败的文件手动编辑为我们希望的内容，在提交。

用`git log --graph`命令可以看到分支合并图

### Bug分支

需求：如果在当前的分支上进行的工作还没有提交，而现在需要修复一个Bug。

对于这种情况，Git提供了一个`stash`功能，可以把当前工作现场"储藏"起来，等以后恢复现场后继续工作。

```shell
$ git stash
Saved working directory and index state WIP on main: ec65d17 & simple
```

现在用`git stash`查看工作区就是干净的（除非有 没有被Git管理的文件）

首先确定要在哪个分支上修复BUG，假定需要在`master`分支上修复，就从`master`创建临时分支；

```shell
git checkout master
# 创建临时bug分支
git checkout -b issue-101
# 开始修复bug，修复完成后提交
git add README.md
git commit -m "fix bug 101"
# 修复完成后，切换到master分支，并完成合并
git switch master
git merge --no-ff -m "merged bug fix 101" issue-101
```

bug修复提交完成后切换回刚刚的工作分支，使用`git stash list`看看刚刚"储藏"的工作区，恢复到工作区有以下两个办法：

* `git stash apply`恢复后，stash内容并不删除，你需要用`git stash drop`来删除
* `git stash pop`恢复的同时把stash内容也清除了

你也可以多次stash，恢复的时候，先用`git stash list`查看，然后指定恢复的stash

```shell
git stash apply stash@{0}
```

假如在master分支修改bug，想要合并到当前dev分支，可以用`git cherry-pick <commit>`命令，把bug 提交的修改"复制"到当前分支，避免重复劳动。

* 建立本地分支和远程分支的关联*`git branch --set-upstream branch-name`

* 从本地推送分支，使用`git push origin branch-name`，如果推送失败，先用`git pull`抓取远程的新提交；
