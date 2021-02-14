const fs = require('fs');
const os = require('os');  

const express = require('express');
const bodyParser = require('body-parser');

const { exec } = require('child_process');
const { sep } = require('path');

const validators = require('./validators');

const app = express();
const tempDirectory = os.tmpdir();
const port = 3000;

// automatically parse POST requests
app.use(bodyParser.urlencoded({extended: true}));
//app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.send('Hello World, from express');
});

app.get('/touch', (req, res) => {
    exec('perl /opt/site/touch.pl');
    res.send('perl');
});

app.post('/ninja', (req, res) => {
    var command = 'perl /opt/Morse-Code-Ninja-main/render.pl ';
    var options = [];
    var input = req.body.source;
    var speeds = req.body.speeds;
    var wordlimit = req.body.wordlimit;
    var test = req.body.test;
    var repeat = req.body.repeat;
    var tone = req.body.tone;
    var sil1 = req.body.sil1;
    var sil2 = req.body.sil2;
    var sil3 = req.body.sil3;
    var extra = req.body.extra;
    var lang = req.body.lang;

    var tempFileName = writeInputToTemp(input);
    console.log(tempFileName);

    options.push('-i');
    options.push(tempFileName);

    options.push('-o');
    options.push('../../../tmp/' + tempFileName.split('/')[2]); // how do I get temp dir out of tempFileName?


    if (speeds) {
        if (!validators.validateSpeeds(speeds)) res.status(500).send('invalid speed parameter');
        options.push('-s');
        options.push(speeds);
    }

    if (wordlimit) {
        if (!validators.validateWordLimit(wordlimit)) res.status(500).send('invalid wordlimit parameter');
        options.push('-l');
        options.push(wordlimit);
    }

    if (test) options.push('--test');
    if (tone) options.push('--tone');

    if (extra) {
        if (!validators.validateExtra(extra)) res.status(500).send('invalid extra parameter');
        options.push('-x');
        options.push(extra);
    }

    if (lang) {
        if (!validators.validateLanguage(lang)) res.status(500).send('invalid language parameter');
        options.push('-l');
        options.push(lang);
    }

    console.log(req.body);
    console.log(command + options.join(' '));

    // kick off perl script and return a "completed" page
    exec(command, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
      });

    res.sendStatus(200);
});

// serve local static content from the public folder
app.use(express.static(__dirname + "/../public"));

app.listen(port, () => {
    console.log(`Morse-Code-Ninja listening at http://localhost:${port}`)
});

function writeInputToTemp(input) {
    var temp = fs.mkdtempSync(`${tempDirectory}${sep}`) + "/input.txt";
    fs.writeFileSync(temp, input);
    return temp;
}