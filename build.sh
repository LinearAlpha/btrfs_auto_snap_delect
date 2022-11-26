# cd ./srv
python3 -OO -m PyInstaller \
    --console \
    --onefile \
    --distpath ./out \
    --specpath ./build \
    --name snap_del \
    ./src/CLArg.py ./src/DelSanp.py ./src/main.py