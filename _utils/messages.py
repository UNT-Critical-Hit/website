def get_apply_message(campaign):
    dm = campaign.get_name() + " [@" + campaign.dm_username + "]"
    addition = ""
    if campaign.current_players >= campaign.max_players:
        addition = """<h5 class="mt-5">You applied to a FULL campaign.</h5>
            <p>
                This means if your application is accepted, you will be added to a <strong>waitlist</strong> for the campaign.
                If a slot opens for the campaign, the next person in the waitlist will be immediately added to the campaign.
                If you ever wish to leave the waitlist, please fill out the Leave a Campaign form found <a target="_blank" href="https://forms.gle/Z4B4huUefwYoBAL67">here</a>.
            </p>
        """
    message = """<h5>What happens next?</h5>
        <p>
            Your application has been sent to the Dungeon Master ({dm}) for review.
            Please give the Dungeon Master some time to review it. You will receive a message on Discord from the UNT Critical Hit
            bot once action has been taken on your application.
        </p>
        {addition}
        <h5 class="mt-5">Have more questions?</h5>
        <p>
            For campaign-related questions, please feel free to reach out to the Campaign Master. You are also more than welcome
            to contact the Dungeon Master of {name} for questions about their campaign.
        </p>
        """.format(dm=dm, addition=addition, name=campaign.name)
    return "Thank you for applying to {name}!".format(name=campaign.name), message

def get_create_message():
    message = """<h5>What happens next?</h5>
        <p>
            Your application has been sent to the Campaign Master for review.
            Please give the Campaign Master some time to review it. You will receive a message on Discord from the UNT Critical Hit
            bot once action has been taken on your application.
        </p>
        <p>
            Please note that once your campaign is created, you will be added to a category in the UNT Critical Hit
            Discord where you will be expected to keep all communications regarding your campaign in. Once your campaign
            is accepted by the Campaign Master, you will receive additional communications on how to add players. 
        </p>
        <h5 class="mt-5">Have more questions?</h5>
        <p>
            For campaign-related questions, please feel free to reach out to the Campaign Master. 
        </p>
        """
    return "Thank you for applying to create a campaign!", message