let data = {};
let charts = {};
let gResults = [];

const init = () => {

  const HEADERS = [
    "議案種類",
    "提出回次",
    "番号",
    "議案件名",
    "審議回次",
    "審議状況",
    "議案提出者"
  ];

  const KEIKA_HEADERS = [
    "審議回次",
    "審議状況",
    "経過情報",
    "経過情報URL",
    "本文情報",
    "本文情報URL",
    "議案種類",
    "議案提出者",
    "衆議院予備審査議案受理年月日",
    "衆議院予備付託年月日／衆議院予備付託委員会",
    "衆議院議案受理年月日",
    "衆議院付託年月日／衆議院付託委員会",
    "衆議院審査終了年月日／衆議院審査結果",
    "衆議院審議終了年月日／衆議院審議結果",
    "衆議院審議時会派態度",
    "衆議院審議時賛成会派",
    "衆議院審議時反対会派",
    "参議院予備審査議案受理年月日",
    "参議院予備付託年月日／参議院予備付託委員会",
    "参議院議案受理年月日",
    "参議院付託年月日／参議院付託委員会",
    "参議院審査終了年月日／参議院審査結果",
    "参議院審議終了年月日／参議院審議結果",
    "公布年月日／法律番号"
  ];

  const KEYWORDS = [
    "ロシア","東日本大震災","新型コロナ","消費税","年金","エネルギー","学校","復興","ウイルス","銀行","郵政","脱税","アメリカ","土地","海上","図書館","関税","大学","子ども","憲法","高齢","漁業","東京","衛生","食品","建築","保育","電波","住宅","科学","証券","沖縄","家族","検察","農林","祝日","燃料","農地","土砂","輸出","スポーツ","国土","教職員","警備","預金","貯金","北海道","鉄道","青少年","インフルエンザ","消防","港湾","医薬","家畜","インド","オリンピック","畜産","患者","テロ","牛肉","鳥獣","衛星","インターネット","扶養","子育て","駐留","パラリンピック","種子"
  ];

  const PARTIES = [
    ["自由民主党","立憲民主党","日本維新の会","公明党","国民民主党","日本共産党","れいわ新選組"],
    ["民主党","社会民主党","自由党","希望の党","民進党","生活の党"]
  ];

  const addCommas = (num) => {
    return String(num).replace( /(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
  }

  const loadData = () => {

    const showData = () => {

      const getParams = (array, dom_id) => {

        // Sort ascending
        let array2 = Object.keys(array).map((k)=>({key: k, value: array[k]}));
        array2.sort((a, b) => a.value - b.value);
        array = Object.assign({}, ...array2.map((item) => ({
          [item.key]: item.value,
        })));

        config_data = [];
        config_labels = [];

        for (let key in array) {
          config_data.push(array[key]);
          config_labels.push(key);
        }

        const params = {
          domid: dom_id,
          labels: config_labels,
          datasets: [{
            name: '',
            data: config_data
          }]
        };

        return params;
      }

      const drawChart = (params) => {
        const $wrapper = $("#" + params.domid);
        const $inner = $wrapper.find(".inner")[0];

        $inner.style.height = 20 + (params.datasets[0].data.length * 20) + "px";
        if (params.domid === "summary-chart-foragainst") $inner.style.height = parseInt($inner.style.height.replace("px", "")) * 1.2 + "px";

        const myChart = echarts.init($inner);
        let option = {
          legend: {
            show: ((params.datasets.length >= 2) ? true: false)
          },
          grid: {
            top: ((params.datasets.length >= 2) ? '40px': '0'),
            left: '3%',
            right: '6%',
            bottom: '3%',
            containLabel: true
          },
          tooltip: {
            show: true,
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            },
            alwaysShowContent: true,
            className: 'echarts-tooltip',
            backgroundColor: 'rgba(0, 0, 0, 0.6)',
            borderWidth: 0,
            padding: [8, 16],
            textStyle: {
              color: "#fefefe",
              fontSize: 13,
            },
            formatter: ((d) => {
              //console.log(d);
              let title = params.labels[d[0].dataIndex];
                if ((params.domid === "summary-chart-committee")
                    &&  (title.substr(-3) !== "審査会")
                    &&  (title !== "審査省略要求")
                  ) {
                    title += "委員会";
                  }
              let value = addCommas(d[0].value);

              let ret = title;
              d.map((r, i) => {
                let prefix = (params.datasets[i].name !== "") ? params.datasets[i].name + "：": "";
                ret += "<br>" + prefix + "<span>" + addCommas(r.value) + "</span> 件"
              });
              return ret;
            })
          },
          xAxis: {
            type: 'value',
            position: 'top',
            splitNumber: 4,
            splitLine: {
              show: true,
              lineStyle: {
                color: '#ccc',
                //miterLimit: 2
              }
            },
            axisLabel: {
              formatter: ((d) => {
                return addCommas(d);
              })
            }
          },
          yAxis: {
            type: 'category',
            data: params.labels.map((label) => {
              const MAX_LABEL_LENGTH = 8;
              let ret = label;
              if (label.length >= MAX_LABEL_LENGTH) ret = label.slice(0, MAX_LABEL_LENGTH - 1) + "…";
              return ret;
            })
          },
          series: []
        };

        params.datasets.map((dataset, i) => {
          option.series.push({
            name: dataset.name,
            type: 'bar',
            stack: 'total',
            label: {
              show: (params.datasets.length === 1) ? true: false,
              position: "right",
              textBorderColor: "#fff",
              textBorderWidth: 0,
              color: "#47a",
              formatter: ((d) => {
                return addCommas(d.data);
              })
            },
            itemStyle: {
              color: (i === 0) ? "#47a": "#f5d25f"
            },
            data: dataset.data
          });
        });

        myChart.setOption(option);
      }

      const updateSelectBox = (file_name, select_id) => {
        const $select = $("#" + select_id);
        for (let key in data[file_name]) {
          const option = '<option value="' + key + '">' + data[file_name][key] + '</option>';
          $select.append(option);
        }
      }

      const updateSelectBoxParties = (select_id) => {
        const $select = $("#" + select_id);

        PARTIES.map((ps, i) => {
          const grouplabel = ["現在の主な政党", "過去の主な政党"][i];
          $select.append('<optgroup label="' + grouplabel + '"></optgroup>');
          ps.map(party => {
            const option = '<option value="' + party + '">' + party + '</option>';
            $select.find("optgroup:last").append(option);
          });
        });
      }

      const showLatestStatus = () => {
        let statuses = {};

        data.gian_summary.map(gian => {
          const status = gian[5];
          if (status !== "") {
            if (!statuses[status]) {
              statuses[status] = 0;
            }
            statuses[status] += 1;
          }
        });

        drawChart(getParams(statuses, 'summary-chart-status'));
      }

      const showCommittees = () => {
        let committees = {};

        data.gian_summary.map(gian => {
          gian[7].map(info => {
            const cominfo = info[11];
            if (cominfo.indexOf("／") !== -1) {
              const name = cominfo.split("／")[1];
              if (name !== "" && name !== "審査省略") {
                if (!committees[name]) {
                  committees[name] = 0;
                }
                committees[name] += 1;
              }
            }
          });
        });

        drawChart(getParams(committees, 'summary-chart-committee'));
      }

      const showSubmitters = () => {
        let submitters = {};

        data.gian_summary.map(gian => {
          let name = gian[6];
          let i = 0;

          if (name.indexOf("君外") !== -1) {
            name = name.split("君外")[0].replace("　", " ");
            i = 1;
          }

          if (name.slice(-1) === "君") {
            name = name.substr(0, -1).replace("　", " ");
            i = 1;
          }

          if (name !== "") {
            if (!submitters[name]) {
              submitters[name] = 0;
            }
            submitters[name] += 1;
          }
        });

        let submitters2 = {};
        for (let key in submitters) {
          const s = submitters[key];
          if (s >= 5) submitters2[key] = s;
        }

        drawChart(getParams(submitters2, 'summary-chart-submitter'));
      }

      const showForAgainst = () => {
        let parties = {};

        PARTIES.map((ps) => {
          ps.map((p) => {
            parties[p] = [0, 0];
          });
        });

        data.gian_summary.map(gian => {
          gian[7].map(row => {
            if (row[15] != "") {
              [row[15], row[16]].map((fas, j) => {
                fas = fas.replaceAll("; ", "／");
                fas = fas.replaceAll(";", "／");
                fas = fas.replaceAll("・", "／");
                fas.split("／").map((party) => {
                  if (party in parties) {
                    parties[party][j] += 1;
                  }
                });
              });
            }
          });
        });

        let array2 = Object.keys(parties).map((k)=>({key: k, for: parties[k][0], agn: parties[k][1]}));
        array2.sort((a, b) => (a.for + a.agn) - (b.for + b.agn));
        parties = Object.assign({}, ...array2.map((item) => ({
          [item.key]: [item.for, item.agn],
        })));

        config_data = [[],[]];
        config_labels = [];

        for (let key in parties) {
          config_data[0].push(parties[key][0]);
          config_data[1].push(parties[key][1]);
          config_labels.push(key);
        }
        //console.log(submitters);

        drawChart({
          domid: 'summary-chart-foragainst',
          labels: config_labels,
          datasets: [{
            name: '賛成',
            data: config_data[0]
          },{
            name: '反対',
            data: config_data[1]
          }]
        });
      }

      const updateKeywords = () => {
        const KEYWORDS_NUM = Math.min(KEYWORDS.length, 6);
        let copy = KEYWORDS.map(d => {
          return d;
        });
        for (let i = 0; i < KEYWORDS_NUM; i++) {
          const j = Math.floor(Math.random() * (KEYWORDS.length - i)); // Between 0 and (KEYWORDS_NUM - 1)
          $("#keywords").append('<a href="">' + copy[j] + '</a>｜');
          copy.splice(j, 1);
        }

        $("#keywords").find("a").on("click", function(e){
          e.preventDefault();
          $("#input-gian-title").val($(this).text());
          $("#form-gian-search").submit();
        });
      }

      updateSelectBox("gian_type", "select-gian-type");
      updateSelectBox("gian_status", "select-gian-status");
      updateSelectBoxParties("select-party-for");
      updateSelectBoxParties("select-party-against");

      showLatestStatus();
      showCommittees();
      showSubmitters();
      showForAgainst();

      updateKeywords();

      $("#cover").fadeOut();
    }

    const updateData = (updatetime) => {

      let count = 0;

      const targets = [
        "updatetime",
        "gian_type",
        "gian_status",
        "gian_summary"
      ];

      targets.map((target) => {
        $.getJSON("data/" + target + ".json", function(json){
          data[target] = json;
          count++;
          if (count >= targets.length) {
            showData();
          }
        });
      });
    }

    if (localStorage.getItem('smri-gian')) {
      data = localStorage.getItem('smri-gian');
      $.getJSON("data/updatetime.json", function(updatetime){
        let t1 = new Date(updatetime.file_update);
        let t2 = new Date(data.updatetime.file_update);
        if (t1 > t2) {
          updateData();
        } else {
          showData();
        }
      });
    } else {
      updateData();
    }
  }

  const showSingleGian = (index) => {
    const $inner = $("#single-gian-content-inner");
    const $keika = $("#single-gian-content-keika").empty();
    const gian = data.gian_summary[parseInt(index)];

    $inner.find("h3").text(gian[3]);
    $("#ul-single-gian-items").empty();

    [0,1,2,4,5,6].map(i => {
      const header = HEADERS[i];
      const value = gian[i];

      const li =  '<li>'
                  + '<div>' + header + '</div>'
                  + '<div>' + value + '</div>'
                + '</li>';

      $("#ul-single-gian-items").append(li);
    });

    gian[7].map(keika => {
      $keika.append('<h4>第' + keika[0] + '回の経過情報</h4>');
      $keika.append('<ul class="keika"></ul>');
      $ul = $keika.find('ul.keika:last');

      for (let i = 1; i < keika.length; i++) {
        let value = keika[i];

        if (i === 2 || i === 4) {
          const url = keika[i + 1];
          if (url.slice(0, 8) === "https://") {
            value = '<a href="' + url + '" target="_blank">' + value + 'へのリンク</a>';
          }
        } else if (i === 3 || i === 5) {
          continue;
        }

        const li =  '<li>'
                    + '<div>' + KEIKA_HEADERS[i] + '</div>'
                    + '<div>' + value + '</div>'
                  + '</li>';

        $ul.append(li);
      }
    });

    $("body").addClass("single-gian-show");
  }

  const bindEvents = () => {

    const matchText = (input, haystack) => {

      const unifyString = (str) => {
        let ret = str;

        // Convert Hiragana into Katakana
        ret = str.replace(/[\u3041-\u3096]/g, function(match) {
          var chr = match.charCodeAt(0) + 0x60;
          return String.fromCharCode(chr);
        });

        // Convert full-width characters into half-width
        ret = ret.replace(/[Ａ-Ｚａ-ｚ０-９]/g, function(s) {
            return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);
        });

        return ret;
      }

      input = unifyString(input);
      haystack = unifyString(haystack);

      const DELIMITERS = ["　", " ", ","];
      const DELIMITER = "／／";

      DELIMITERS.map(d => {
        input = input.replace(d, DELIMITER);
        haystack = haystack.replace(d, "");
      });

      const words = input.split(DELIMITER);
      let match = true;

      words.map((w) => {
        if (haystack.indexOf(w) === -1) match = false;
      });

      return match;
    }

    const matchParty = (input, haystack) => {
      if (input == "") return true;
      if (haystack == "") return false;
      haystack = haystack.replaceAll("・", "／");
      haystack = haystack.replaceAll("; ", "／");
      haystack = haystack.replaceAll(";", "／");
      let ret = false;
      const parties = haystack.split("／");
      if (parties.indexOf(input) !== -1) ret = true;
      return ret;
    }

    $("#form-gian-search").on("submit", function(e){
      e.preventDefault();
      $("#ul-gian-list").empty();

      let gian_results = 0;
      let keika_results = 0;
      let type   = $("#select-gian-type").find("option:selected").text();
      let status = $("#select-gian-status").find("option:selected").text();
      if (type   === "指定なし") type   = "";
      if (status === "指定なし") status = "";
      const title = $("#input-gian-title").val();
      const submitter = $("#input-gian-submitter").val();
      const party_f = $("#select-party-for").val();
      const party_a = $("#select-party-against").val();
      const MAX_RESULTS = 1000;
      gResults = [];

      for (let i = 0; i < data.gian_summary.length; i++) {
        const gian = data.gian_summary[i];

        let hit = true;

        hit = matchText(title, gian[3]);

        if (!matchText(submitter, gian[6])) hit = false;
        if (gian[0].indexOf(type) === -1) hit = false;
        if (gian[5].indexOf(status) === -1) hit = false;

        gian[7].map(keika => {
          if (!matchParty(party_f, keika[15])) hit = false;
          if (!matchParty(party_a, keika[16])) hit = false;
        });

        if (hit) {
          gian_results  += 1;
          keika_results += gian[7].length;
          gResults.push(gian);

          if (gian_results <= MAX_RESULTS) {
            const li =  '<li index="' + i + '">'
                        + '<div><span>第' + gian[4] + '回国会</span> ' + gian[5] + '</div>'
                        + '<div>' + gian[3] + '</div>'
                        + '<div>提出：第' + gian[1] + '回国会｜' + gian[0] + '</div>'
                      + '</li>';
            $("#ul-gian-list").append(li);
          }
        }
      }

      if (gian_results > MAX_RESULTS) {
        $("#result-number").text(addCommas(gian_results) + "件ヒットしました。" + addCommas(MAX_RESULTS) + "件までを表示しています。");
      } else if (gian_results === 0) {
        $("#result-number").text("該当する議案がありませんでした。");
      } else {
        $("#result-number").text(addCommas(gian_results) + "件ヒットしました。");
      }

      if (gian_results === 0) {
        $("#download-result").text("");
      } else {
        $("#download-result").text("検索結果（途中経過含め" + keika_results + "件）をCSVでダウンロードする");
      }


      $("li").on("click", function(){
        showSingleGian($(this).attr("index"));
      });
    });

    $("#single-gian-cover").on("click", function(){
      $("body").removeClass("single-gian-show");
    });

    $("#single-gian-button-close").on("click", function(){
      $("body").removeClass("single-gian-show");
    });

    $("#switch").find(".switch-item").on("click", function(){
      if (!$(this).hasClass("selected")) {
        $(this).siblings(".switch-item").removeClass("selected");
        $(this).addClass("selected");

        $("#switch").find(".switch-item").each(function(){
          let code = $(this).attr("code");
          if ($(this).hasClass("selected")) {
            $("#" + code + "-block").addClass("show");
          } else {
            $("#" + code + "-block").removeClass("show");
          }

          $('body, html').scrollTop(0);
        });
      }
    });

    $("#download-result").on("click", function(e){
      e.preventDefault();

      const getResultsToArray = () => {
        let headers = HEADERS.concat(KEIKA_HEADERS);
        headers.splice(4, 2);
        let data = headers.join(",") + "\n";

        gResults.map(row => {
          row[7].map((keikarow, i) => {
            data += [row[0], row[1], row[2], row[3], row[6]].join(",") + "," + keikarow.join(",") + "\n";
          });
        });

        return data;
      }

      const now = new Date();
      const y = now.getFullYear();
      const m = now.getMonth()+1;
      const d = now.getDate();
      const h = now.getHours();
      const n = now.getMinutes();
      const s = now.getSeconds();
      const data = getResultsToArray();
      const filename = "smri-national-diet-bills-" + y + m + d + h + n + s + ".csv";
      const bom = new Uint8Array([0xef, 0xbb, 0xbf]);
      const blob = new Blob([bom, data], {type: "text/csv"});

      if (window.navigator.msSaveBlob) {
        window.navigator.msSaveBlob(blob, filename);
      } else {
        const url = (window.URL || window.webkitURL).createObjectURL(blob);
        const d = document.createElement("a");
        d.href = url;
        d.download = filename;
        d.click();
        (window.URL || window.webkitURL).revokeObjectURL(url);
      }
    });

    $("#social-button-copy").on("click", function(e){
      e.preventDefault();
      let text = "国会議案データベース - スマートニュース メディア研究所\nhttps://smartnews-smri.github.io/national-diet-bills/";
      let $textarea = $('<textarea></textarea>');
      $textarea.text(text);
      $(this).append($textarea);
      $textarea.select();
      document.execCommand('copy');
      $textarea.remove();
      let $copyText = $(this).next(".text-copy");
      $copyText.addClass("copied");

      setTimeout(function() {
        $copyText.removeClass("copied");
      }, 3000);
    });
  }

  loadData();
  bindEvents();
}


$(function(){
  init();
});
