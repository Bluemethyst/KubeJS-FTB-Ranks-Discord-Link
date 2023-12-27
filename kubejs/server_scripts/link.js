console.info('Hello, World! (Loaded Discord Link)')

const new_json = JsonIO.read('brass_players.json')

ServerEvents.loaded(event => {
    event.server.runCommandSilent('ftbranks create Brass')
    event.server.scheduleInTicks(6000, ctx => {
        if (new_json && new_json.players) {
            new_json.players.forEach(member => {
                if (member.mc_username) {
                    console.info ('Updated FTB Ranks supporter ranks')
                    event.server.runCommandSilent(`ftbranks add ${member.mc_username} Brass`)
                    ctx.reschedule()
                } else {
                    console.error('error, please contact Bluemethyst')
                }
            })
        } else {
            console.error('Failed to read brass_players.json')
            console.error('error')
        }
    })
})

ServerEvents.customCommand()
