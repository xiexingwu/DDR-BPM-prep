
predeploy:
	bash $(PROJ_DIR)/scripts/deploy/predeploy.sh

predeploy-force: export FORCE=Y
predeploy-force: predeploy
