
predeploy:
	bash $(PROJ_DIR)/scripts/deploy/predeploy.sh


# deploy: lowres
# 	git push
# 	git tag vAuto --force
# 	git push origin vAuto --force
#
# zip: hash
# 	zip data.zip -qr data || [ $$? -eq 12 ]
# 	zip jackets.zip -qr jackets-lowres || [ $$? -eq 12 ]
# 	zip simfiles.zip -qr simfiles || [ $$? -eq 12 ]
#
# hash:
# 	bash ./bin/hashSongs.sh > hashed_songs.txt
# 	bash ./bin/hashJackets.sh > hashed_jackets.txt
# 	bash ./bin/hash.sh courses.json > hashed_courses.txt

