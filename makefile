default: vm

# Reinstall the VM
reinstall: clean vm

# Clean everything to pristine conditions
clean:
	# Destroy the VM and delete .vagrant
	vagrant destroy --force
	@rm -rf .vagrant

	# Remove ansible roles downloaded from galaxy
	@rm -rf provisioning/roles/lvps.389ds_server

	# Remove generated openssl generated files
	@rm -f provisioning/files/fullchain-certificate.pem
	@rm -f provisioning/files/tls.key
	@rm -f provisioning/files/openssl/noise.bin

# Create the VM
vm:
	# Download ansible roles
	@ansible-galaxy install --roles-path provisioning/roles lvps.389ds_server

	# Generate certificates
	@cd provisioning && ./cert.sh localhost

	# Spin up the machine
	vagrant up

identities:
	cd provisioning && ./idgen.py

provision:
	vagrant provision