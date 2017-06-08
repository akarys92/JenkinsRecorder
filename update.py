from main import Main


def run():
    print "Running for public..."
    public = Main('config/config.json')
    public.updateData()

    print "Running for Sovereign..."
    nc = Main('config/NcConfig.json')
    nc.updateData()

    print "Done!"

run()
