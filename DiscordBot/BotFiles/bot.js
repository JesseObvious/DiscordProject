
// DMONEY made dis
// 12/4/2021

var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
const fs = require('fs');
const userName = "plex";

var botResponses =  [
    'You realize this movies dogshit right?',
    'Not bad.. brb',
    'Not what I would have picked..',
    'really??',
    'Peach ice tea. Youre gonna hate it.',
    'No one wants to watch this shit btw',
    'dis movie hotter than a hoochie coochie',
    'kinda sus but ok..',
    'Finally a decent pick..',
    'dis movie booty btw',
    'Ill download it but i aint watchin this shit',
    'what is wrong with you?',
    'I hope yall ready to buffer',
    'nah im good',
    'who gave this dumbass permission to search?',
    'I am dead inside',
    'somebody making soup?',
    'I hate so much.. about the things that you choose to be.'


];

var botResponses2 =  [
    'ight fuck you too then',
    'thanks for wasting my goddamn time',
    'good choice',
    'youre better off without this one honestly',
    'try again bitch',
    'A small fan could have been powered in africa, but you chose to waste my electricity',

];

var randomIndex = Math.floor(Math.random()*botResponses.length);
var randomElement = botResponses[randomIndex];

var randomIndex2 = Math.floor(Math.random()*botResponses2.length);
var randomElement2 = botResponses2[randomIndex2];



function movieExistsCheck(channelID) {

    const { spawn } = require('child_process');
    const pp = spawn('python3', ['/home/' + userName + '/DiscordProject/DiscordBot/SourceCode/PopulateHistory.py']);
                    
    pp.stdout.on('data', (data) => {
        console.log(`stdout - movieExistsCheck: ${data}`);
    
        bot.sendMessage({
            to: channelID,
            message: data
        });
                
    });

    pp.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });

    pp.on('close', (code) => {
        console.log(`movieExistsCheck child process exited with code ${code}`);
        
    });
}

function cleanTexts() {

    const { spawn } = require('child_process');
    const pp = spawn('python3', ['/home/' + userName + '/DiscordProject/DiscordBot/SourceCode/clean.py']);
                    
    pp.stdout.on('data', (data) => {
        console.log(`stdout - cleanTexts: ${data}`);
                
    });

    pp.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });

    pp.on('close', (code) => {
        console.log(`cleanTexts child process exited with code ${code}`);
    });
}
   
function fileSizeCheck(channelID) {

    const { spawn } = require('child_process');
    const pp = spawn('python3', ['/home/' + userName + '/DiscordProject/PythonPlex/SourceCode/fileSizeCheck.py']);
                    
    pp.stdout.on('data', (data) => {
        console.log(`stdout - fileSizeCheck: ${data}`);
        bot.sendMessage( {
            to: channelID,
            message: data
        });        
    });

    pp.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });

    pp.on('close', (code) => {
        console.log(`cleanTexts child process exited with code ${code}`);
        
    });
}
   

// executes the download python script
function downloadScriptCall(channelID, user, userID) {

    const { spawn } = require('child_process');
    const pp = spawn('python3', ['/home/' + userName + '/DiscordProject/PythonPlex/SourceCode/Download.py']);
                    
    pp.stdout.on('data', (data) => {
        console.log(`stdout - downloadScriptCall: ${data}`);
    });

    pp.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
        
    });

    pp.on('close', (code) => {
        console.log(`downloadScriptCall child process exited with code ${code}`);
        
        bot.sendMessage({
            to: channelID,
            message: ('The movie should be on the Plex server now <@' + userID + '>')
    
        });
        

    });
}

//finds more titles from tpb

function moreTitles(channelID) {

    const { spawn } = require('child_process');
    const pp = spawn('python3', ['/home/' + userName + '/DiscordProject/PythonPlex/SourceCode/MultipleResults.py']);
    
    // prints out the movie link
    pp.stdout.on('data', (data) => { 
        console.log('stdout - moreTitlesCall: ${data}');
        bot.sendMessage( {
            to: channelID,
            message: data
        });
    });

    // prints when error has occured
    pp.stderr.on('data', (data) => {
        console.log('stderr: ${data}');
    });

    // prints when program has closed
    pp.on('close', (code) => {
        console.log('moreTitlesScriptCall child process exited with code ${code}');

        //randomizing the asshole bot responses
        randomIndex = Math.floor(Math.random()*botResponses.length);
        randomElement = botResponses[randomIndex];

        randomIndex2 = Math.floor(Math.random()*botResponses2.length);
        randomElement2 = botResponses2[randomIndex2];

    });

}
        

// executes the python script that checks the top movie link searched
function pirateScriptCall(channelID, user, userID) {
    const { spawn } = require('child_process');
    const pp = spawn('python3', ['/home/' + userName + '/DiscordProject/PythonPlex/SourceCode/Pirate.py']);
    
    // prints out the movie link
    pp.stdout.on('data', (data) => { 
        console.log('stdout - pirateScriptCall: ${data}');
        

        bot.sendMessage( {
            to: channelID,
            message: data
        });
    });

    // prints when error has occured
    pp.stderr.on('data', (data) => {
        console.log('stderr: ${data}');
    });

    // prints when program has closed
    pp.on('close', (code) => {
        console.log('pirateScriptCall child process exited with code ${code}');

        //randomizing the asshole bot responses
        randomIndex = Math.floor(Math.random()*botResponses.length);
        randomElement = botResponses[randomIndex];

        randomIndex2 = Math.floor(Math.random()*botResponses2.length);
        randomElement2 = botResponses2[randomIndex2];

        if(fs.existsSync('/home/' + userName + '/DiscordProject/DiscordBot/TxtFiles/GoodToGo.txt')) {
            bot.uploadFile( {
                to: channelID,
                file: '/home/' + userName + '/DiscordProject/PythonPlex/Art/pic.jpg'
            });
        }
        
    });

}

    // Configure logger settings
    logger.remove(logger.transports.Console);
    logger.add(new logger.transports.Console, {
        colorize: true
    });
    logger.level = 'debug';
    // Initialize Discord Bot
    var bot = new Discord.Client({
    token: auth.token,
    autorun: true
    });

    bot.on('ready', function (evt) {
        logger.info('Connected');
        logger.info('Logged in as: ');
        logger.info(bot.username + ' - (' + bot.id + ')');
    });

bot.on('message', function (user, userID, channelID, message, evt) {

// Our bot needs to know if it will execute a command
// It will listen for messages that will start with `!`
    if (message.substring(0, 1) == '!') {
        var args = message.substring(1);
        var cmd = args;
        
        if(cmd != 'yes' || cmd != 'no') {
            movieHistory = cmd;
        }
        
        switch(cmd) {
            
            //checking for user to reply yes
            case 'yes':

                bot.sendMessage({
                    to: channelID,
                    message: "Making sure this movie checks out.."
                });

                movieExistsCheck(channelID);

                fileSizeCheck(channelID);

                if(fs.existsSync('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/FileTooBig.txt')) {
                    if(fs.existsSync('/home/' + userName + '/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt')) {
                    
                                     
                    }
    
                    else {
                        bot.sendMessage({
                            to: channelID,
                            message: "There aren't enough seeds dummy.. Try something else"
                                        
                        });
                        
                    }               
                }

                else {
                    bot.sendMessage({
                        to: channelID,
                        message: "File size is too big.. check with admin if you really want this"
                                    
                    });

                }

            
                break;
                    
            case 'no':

                cleanTexts();
                bot.sendMessage({
                    to: channelID,
                    message: randomElement2
                });


                break;
            
            case 'more':

                bot.sendMessage({
                    to: channelID,
                    message: 'Finding more options..'
                });

                moreTitles(channelID);

                break;

            case '1':
                var choice1 = fs.readFileSync('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/Choices/1.txt');

                fs.writeFile('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/DownloadLink.txt', choice1, (err) => {
                
                    if (err) throw err;
                });
                
                bot.sendMessage({
                    to: channelID,
                    message: "Making sure this file checks out.."
                });

                movieExistsCheck(channelID);

                fileSizeCheck(channelID);
                
                

                break;
            
            case '2':
                var choice2 = fs.readFileSync('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/Choices/2.txt');

                fs.writeFile('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/DownloadLink.txt', choice2, (err) => {
                
                    if (err) throw err;
                });                
 
                bot.sendMessage({
                    to: channelID,
                    message: "Making sure this file checks out.."
                });

                movieExistsCheck(channelID);

                fileSizeCheck(channelID);

                break;

            case '3':
                var choice3 = fs.readFileSync('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/Choices/3.txt');

                fs.writeFile('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/DownloadLink.txt', choice3, (err) => {
                
                    if (err) throw err;
                });

                bot.sendMessage({
                    to: channelID,
                    message: "Making sure this file checks out.."
                });

                movieExistsCheck(channelID);

                fileSizeCheck(channelID);

                break;

            case '4':
                var choice4 = fs.readFileSync('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/Choices/4.txt');

                fs.writeFile('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/DownloadLink.txt', choice4, (err) => {
                
                    if (err) throw err;
                });
                
                bot.sendMessage({
                    to: channelID,
                    message: "Making sure this file checks out.."
                });

                movieExistsCheck(channelID);

                fileSizeCheck(channelID);

                break;

            case '5':
                var choice5 = fs.readFileSync('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/Choices/5.txt');

                fs.writeFile('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/DownloadLink.txt', choice5, (err) => {
                
                    if (err) throw err;
                });
                
                bot.sendMessage({
                    to: channelID,
                    message: "Making sure this file checks out.."
                });

                movieExistsCheck(channelID);

                fileSizeCheck(channelID);

                break;

            case 'download':
                               
                if(fs.existsSync('/home/' + userName + '/DiscordProject/PythonPlex/TxtFiles/FileTooBig.txt')) {
                    if(fs.existsSync('/home/' + userName + '/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt')) {
                        bot.sendMessage({
                            to: channelID,
                            message: "Downloading.. This should take 10-30 minutes"
                        
                        });  

                        bot.sendMessage({
                            to: channelID,
                            message: "If it takes longer than 30 minutes contact dmoney"
                        
                        });  
                        

                        //starting download
                        downloadScriptCall(channelID, user, userID);            
                    }

                    else {
                        bot.sendMessage({
                            to: channelID,
                            message: "What did I just say??\nYou really tryna break this fuckin bot aint ya bitch?"
                        
                        });   
                    }
                }
                
                else {
                    bot.sendMessage({
                        to: channelID,
                        message: "What did I just say??\nYou really tryna break this fuckin bot aint ya bitch?"
                    
                    });   
                }
                        
                break;
                
            
            case 'fuck you':
                bot.sendMessage({
                    to: channelID,
                    message: "No you fuck me ;)"
                });

                break;
                    
            default:
                            
                //checking if user wants queue of titles
                if(cmd.includes('+')) {
                    let n = (cmd.split('+').length - 1);
                    for(let i = 0; i <= n; i++) {
                        let tmpTitle = cmd.split('+');
                        if(i == 0) {
                            fs.writeFile('/home/' + userName + '/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt', tmpTitle[i] + '\n', (err) => {
                    
                                if (err) throw err;
                            });
                        }

                        else {
                            fs.appendFile('/home/' + userName + '/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt', tmpTitle[i] + '\n', (err) => {
                                if(err) throw err;
                            });
                        }
                    }
                    
                    bot.sendMessage({
                        to: channelID,
                        message: randomElement
                    });
                    
                    break;
                }

                // Write data in 'Output.txt' .
                fs.writeFile('/home/' + userName + '/DiscordProject/DiscordBot/TxtFiles/MovieTitle.txt', cmd, (err) => {
                
                    if (err) throw err;
                });
                
            
                bot.sendMessage({
                    to: channelID,
                    message: randomElement
                });

                // fetching movie
                pirateScriptCall(channelID);
                
                

            
            break;

        }
    
        
    }
    
});

