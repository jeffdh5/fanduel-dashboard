var PlayerCard = React.createClass({
	
	createStatTable: function(headers, data) {
		//console.log('data', data)
		//console.log('headers', headers)
		var headers = headers.map(function(header) {
			//console.log('hello', header)
			return (
				<th>{header}</th>
			)
		});
		var tableRows = data.map(function(rows) {
			//console.log('rows', rows)
			var tableCells = rows.map(function(cellValue) {
				return (
					<td>{cellValue}</td>
				)				
			});
			
			return (
				<tr>
					{tableCells}
				</tr>
			)

		});

		return (
	    	<table className="table table-bordered player-stat-table">
	    		<thead>
	      			<tr>
	        			{headers}
	      			</tr>
	    		</thead>
	    		<tbody>
	    			{tableRows}
	    		</tbody>
	    	</table>
		)
	},

	render: function() {
		//console.log('hello', this.props.playerData)
		var commentNodes = this.props.playerData.player_comments.map(function(comment) {
			return (
    			<p>{comment}</p>
			)
		});	
		var headers = ['Date', 'OPP', 'PTS', 'MP', 'BS', 'A', 'ST', 'REB', 'TO', 'FPS']
		var lastFiveGamesTable = this.createStatTable(headers, this.props.playerData.player_data.last_5_games);
		
		// Note: Avg'ed and STD data is only one dimensional, so wrap it in an array so that you can feed it 
		// into the 2D stat table generator method written above.

		var lastFiveAvgTable = null;
		var lastFiveStdTable = null;

		var headersWithoutTextColumns = ['PTS', 'MP', 'BS', 'A', 'ST', 'REB', 'TO', 'FPS']

		if (this.props.playerData.player_data.last_5_games_avg) {
			lastFiveAvgTable = this.createStatTable(headersWithoutTextColumns, [this.props.playerData.player_data.last_5_games_avg]);
		}
		if (this.props.playerData.player_data.last_5_games_std)
			lastFiveStdTable = this.createStatTable(headersWithoutTextColumns, [this.props.playerData.player_data.last_5_games_std]);
		
		var salary = this.props.playerData.player_data.fanduel_salary;
		var FPPG = this.props.playerData.player_data.FPPG;
		var target = Math.round(salary / 220 * 100)/100;
		var position = this.props.playerData.player_data.position;
		var name = this.props.playerData.player_data.name;
		var injuryStatus = this.props.playerData.player_data.is_injured;
		var comments = this.props.playerData.player_comments;

		return (
			<div className="player-card">
				<div className="panel panel-default">
					<div className="panel-heading">
						<span><b> {name} </b> </span> | 
						<span> Position: <u>{position}</u> </span> | 
						<span> Salary: <u>{salary}</u> </span> | 
						<span className={(FPPG > target) ? 'greenlight' : 'redlight'}> FPPG: <u>{FPPG}</u> </span> | 
						<span> Target: <u>{target}</u></span>
					</div>

  					<div className="panel-body">
  						<p>{(comments.length > 0) ? "Expert Analysis: " : ""}</p>
  						{commentNodes}
  						<span>{injuryStatus ? 'Injury Status: ' : ''}</span> 
  						<span className='redlight'> {injuryStatus ? 'Sidelined' : ''}</span>
  						<p>Last Five Games:</p>
  						{lastFiveGamesTable}
  						<p>Last Five Average:</p>
  						{lastFiveAvgTable}
  						<p>Last Five Standard Deviation:</p>
  						{lastFiveStdTable}

					</div>
				</div>
			</div>
		)
	}
})

var GameCard = React.createClass({
	render: function() {
		return (
  			<div className="btn-group" role="group">
    			<button type="button" className="btn btn-default" onClick={this.props.onGameCardClick.bind(this, this.props.gameData.query_url)}>
    				<div>
    					<div className="home">{this.props.gameData.home} at</div>
    					<div className="away">{this.props.gameData.away}</div>
    				</div>
       			</button>
  			</div>
		)

	}
})

var Dashboard = React.createClass({

	getInitialState: function() {
		return {coreLineup: {home: [], away: []}}
		//return {data: [], teamQueryURL: ''};
	},

	componentDidMount: function() {

	},

	handleClick: function(queryURL) {
		//this.setState({teamQueryURL: queryURL});
		$.get(queryURL+'/core_lineup', function(result) {
			//console.log('result', result)
        	this.setState({coreLineup: JSON.parse(result)});
        	//console.log(teamData);
        }.bind(this));	
	},

	render: function() {

		return (
			<div className="dashboard">
				<GameViewer onGameCardClick={this.handleClick}/>
				<CompareTool coreLineup={this.state.coreLineup} />
			</div>
		);
	}
})


var GameViewer = React.createClass({
	getInitialState: function() {
		return {gameData: []}
	},

	componentDidMount: function() {
		$.get('/todays_games', function(result) {
      		if (this.isMounted()) {
        		this.setState({gameData: JSON.parse(result)});
        	}
        }.bind(this));
	},

	render: function() {

		var gameCardNodes = this.state.gameData.map(function(entry) {
			return (
				<GameCard gameData={entry} onGameCardClick={this.props.onGameCardClick}/>
			)
		}.bind(this));

		return (
			<div className="game-card-container">
				<div className="btn-group btn-group-justified" role="group">
					{gameCardNodes}
				</div>
			</div>
		)
	}
})


var PlayerPool = React.createClass({
	getInitialState: function() {
		return {player_pool: []}
	},

	loadData: function() {

		$.get('/player_pool', function(result) {
			//console.log('result', result)
      		if (this.isMounted()) {
        		this.setState({player_pool: JSON.parse(result)});
        		//console.log(teamData);
        	}
        }.bind(this));	
	},

	componentDidMount: function() {
		this.loadData();
	},

	componentDidUpdate: function() {
		this.loadData();
	},

	render: function() {

		var playerNodes = this.state.player_pool.map(function(entry) {
			return (
				<PlayerCard playerData={entry} />
			)
		});

		return (
			<div>
				{playerNodes}
			</div>

		)

	}



})

var CompareTool = React.createClass({


	render: function() {


		if (this.props.coreLineup.home.length == 0 || this.props.coreLineup.away.length == 0) {
			console.log('woah')
			return (
				<div className="compare-tool">
					<div className="compare-tool-header">
						<h1>Compare Tool</h1>
						<p>No team has been selected yet.</p>
					</div>
				</div>
			)
		}
		console.log(this.props.coreLineup)
		var awayPlayerNodes = this.props.coreLineup.away.map(function(entry) {
			//console.log(entry)
			return (
				<PlayerCard playerData={entry} />
			)
		});

		var homePlayerNodes = this.props.coreLineup.home.map(function(entry) {
			return (
				<PlayerCard playerData={entry} />
			)
		});

		return (
			<div className="compare-tool">
				<div className="compare-tool-header">
				</div>
				<div className="compare-tool-team">
					{homePlayerNodes}
				</div>

				<div className="compare-tool-team">
					{awayPlayerNodes}
				</div>
			</div>

		)

	}
})


React.render(
  <Dashboard pollInterval={1000} base_url='/query' />,
  document.getElementById('content')
);