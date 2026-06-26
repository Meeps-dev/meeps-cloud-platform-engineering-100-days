# Day 40: Backups, Snapshots, Parameter Groups, and Multi-AZ

## What I Learned

- Automated backups help protect RDS data and support recovery.
- Backup retention controls how long AWS keeps automated backups.
- Manual snapshots are backups created manually before risky changes.
- Restoring a snapshot creates a new RDS database instead of overwriting the existing one.
- Multi-AZ improves database availability by keeping a standby database in another Availability Zone.
- Multi-AZ is mainly for failover, not read scaling.
- Parameter groups control database engine settings.
- Some database settings are dynamic and apply immediately.
- Static parameter changes usually require a database reboot.

## What I Did

- Confirmed automated backups were enabled.
- Reviewed the backup retention period.
- Created a manual RDS snapshot.
- Reviewed the Multi-AZ option.
- Inspected the current DB parameter group.
- Created/reviewed a custom parameter group for better understanding.
- Checked which parameter changes require a reboot.

## What I Broke

- I tested the backup and restore process by creating a manual snapshot.
- I reviewed how restoring from a snapshot works with a temporary RDS instance.
- I checked how parameter group changes can enter a pending reboot state.

## How I Fixed It

- Confirmed the manual snapshot was available.
- Verified that restore creates a separate temporary database.
- Confirmed the main RDS database was not overwritten.
- Deleted the temporary restored database after testing to avoid extra cost.
- Documented that static parameter changes require a reboot, while dynamic changes can apply immediately.

## Key Takeaway

- RDS backups and snapshots are important for database recovery.
- Parameter groups should be changed carefully.
- Multi-AZ improves availability, but it can increase cost.
- Temporary restore tests should be cleaned up after screenshots.
