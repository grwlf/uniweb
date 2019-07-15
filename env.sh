export CWD=`pwd`
export PYTHONPATH="$CWD/src:$PYTHONPATH"
export MYPYPATH="$PYTHONPATH"
alias ipython="sh $CWD/ipython.sh"

runjupyter() {
  jupyter-notebook --ip 0.0.0.0 --port 8888 \
    --NotebookApp.token='' --NotebookApp.password='' "$@" --no-browser
}
alias jupyter=runjupyter

runtensorboard() {(
  mkdir $CWD/_logs 2>/dev/null
  echo "Tensorboard logs redirected to $CWD/_logs/tensorboard.log"
  tensorboard --logdir=$CWD/_logs "$@" >"$CWD/_logs/tensorboard.log" 2>&1
) & }

runchrome() {(
  mkdir -p $HOME/.chrome_mrc-nlp || true
  chromium \
    --user-data-dir=$HOME/.chrome_mrc-nlp \
    --explicitly-allowed-ports=`seq -s , 6000 1 6020`,`seq -s , 8000 1 8020` \
    http://127.0.0.1:`expr 6000 + $UID - 1000` "$@"
)}

runvim() {(
  if test -x "$EDITOR"; then
    if which pyls >/dev/null 2>&1 && ! ps | grep -v grep | grep pyls ; then
      echo "Running pyls"
      pyls &
    else
      echo "Not running pyls"
    fi
    $EDITOR "$@"
  else
    echo "EDITOR is not executable"
  fi
)}


docnews() {
  ndays="$1"
  test -z "$ndays" && ndays=3
  rev=$(git log -1 --before=@{"$ndays".days.ago} --format=%H)
  docs=`git diff --name-status  --oneline "$rev" | grep -v '^D' | grep -E 'doc|\.md$' | awk '{print $2}'`
  git diff "$rev" -- $docs
}

runomniboard() {(
  db_name="$1"
  mkdir $CWD/_logs 2>/dev/null
  echo "Omniboard logs redirected to $CWD/_logs/omniboard.log"
  omniboard -m "172.17.0.1:27017:$db_name" >"$CWD/_logs/omniboard.log" 2>&1
)& }

cudarestart() {
  sudo rmmod nvidia_uvm ; sudo modprobe nvidia_uvm
}
